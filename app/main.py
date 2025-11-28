"""
API para Geração de Propostas Comerciais Solar
Level5 Engenharia Elétrica

Porta: 3493
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import base64
import os
import uuid
from datetime import datetime

from app.models.proposta import PropostaRequest, PropostaResponse
from app.services.pdf_generator import PDFGenerator
from app.services.graficos import GraficoService
from app.services.calculos import CalculoService

app = FastAPI(
    title="API Gerador de Propostas Solar",
    description="API para geração automática de propostas comerciais para sistemas fotovoltaicos",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretório para arquivos gerados
OUTPUT_DIR = "/tmp/propostas"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "api": "Gerador de Propostas Solar",
        "versao": "1.0.0",
        "status": "online",
        "endpoints": {
            "gerar_proposta": "POST /api/v1/proposta/gerar",
            "health": "GET /api/v1/health",
            "download": "GET /api/v1/download/{filename}"
        }
    }


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "proposta-solar-api"
    }


@app.post("/api/v1/proposta/gerar", response_model=PropostaResponse)
async def gerar_proposta(request: PropostaRequest):
    """
    Gera uma proposta comercial em PDF personalizada.
    
    Recebe os dados do cliente, sistema, investimento, produção mensal
    e retorno do investimento, gerando um PDF completo com gráficos.
    """
    try:
        # Instanciar serviços
        calculo_service = CalculoService()
        grafico_service = GraficoService()
        pdf_generator = PDFGenerator()
        
        # Calcular valores derivados
        investimento_total = request.investimento.kit_fotovoltaico + request.investimento.mao_de_obra
        
        # Encontrar ano do payback (primeiro saldo positivo)
        ano_payback = None
        valor_payback = None
        for item in request.retorno_investimento:
            if item.saldo > 0:
                ano_payback = item.ano
                valor_payback = item.saldo
                break
        
        # Economia em 25 anos (último saldo)
        economia_25_anos = request.retorno_investimento[-1].saldo if request.retorno_investimento else 0
        
        # Gerar gráfico de produção
        grafico_producao_path = grafico_service.gerar_grafico_producao(
            dados_producao=request.producao_mensal,
            quantidade_modulos=request.sistema.modulos.quantidade,
            output_dir=OUTPUT_DIR
        )
        
        # Gerar tabela de retorno como imagem
        tabela_retorno_path = grafico_service.gerar_tabela_retorno(
            dados_retorno=request.retorno_investimento,
            output_dir=OUTPUT_DIR
        )
        
        # Gerar nome único para o PDF
        nome_arquivo = f"proposta_{request.cliente.nome.lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}.pdf"
        pdf_path = os.path.join(OUTPUT_DIR, nome_arquivo)
        
        # Gerar PDF
        pdf_generator.gerar_proposta(
            cliente=request.cliente,
            sistema=request.sistema,
            investimento=request.investimento,
            investimento_total=investimento_total,
            grafico_producao_path=grafico_producao_path,
            tabela_retorno_path=tabela_retorno_path,
            ano_payback=ano_payback,
            valor_payback=valor_payback,
            economia_25_anos=economia_25_anos,
            output_path=pdf_path
        )
        
        # Ler PDF e converter para base64
        with open(pdf_path, "rb") as f:
            pdf_base64 = base64.b64encode(f.read()).decode("utf-8")
        
        # Limpar arquivos temporários de gráficos
        if os.path.exists(grafico_producao_path):
            os.remove(grafico_producao_path)
        if os.path.exists(tabela_retorno_path):
            os.remove(tabela_retorno_path)
        
        return PropostaResponse(
            success=True,
            message="Proposta gerada com sucesso",
            pdf_filename=nome_arquivo,
            pdf_url=f"/api/v1/download/{nome_arquivo}",
            pdf_base64=pdf_base64,
            dados_calculados={
                "investimento_total": investimento_total,
                "ano_payback": ano_payback,
                "valor_payback": valor_payback,
                "economia_25_anos": economia_25_anos
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar proposta: {str(e)}")


@app.get("/api/v1/download/{filename}")
async def download_proposta(filename: str):
    """Download do PDF gerado"""
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf"
    )


@app.post("/api/v1/graficos/producao/preview")
async def preview_grafico_producao(request: PropostaRequest):
    """
    Gera apenas o gráfico de produção para preview.
    Retorna a imagem em base64.
    """
    try:
        grafico_service = GraficoService()
        
        grafico_path = grafico_service.gerar_grafico_producao(
            dados_producao=request.producao_mensal,
            quantidade_modulos=request.sistema.modulos.quantidade,
            output_dir=OUTPUT_DIR
        )
        
        with open(grafico_path, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode("utf-8")
        
        os.remove(grafico_path)
        
        return {
            "success": True,
            "image_base64": img_base64,
            "format": "png"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3493)
