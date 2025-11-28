"""
Modelos Pydantic para validação de dados da API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any


class ClienteModel(BaseModel):
    """Dados do cliente"""
    nome: str = Field(..., description="Nome do cliente")


class ModulosModel(BaseModel):
    """Dados dos módulos fotovoltaicos"""
    quantidade: int = Field(..., ge=1, description="Quantidade de módulos")
    marca: str = Field(..., description="Marca do módulo")
    potencia_w: int = Field(..., ge=1, description="Potência em Watts")
    tipo: str = Field(default="Mono", description="Tipo do módulo (Mono/Poly)")


class InversoresModel(BaseModel):
    """Dados dos inversores"""
    quantidade: int = Field(..., ge=1, description="Quantidade de inversores")
    marca: str = Field(..., description="Marca do inversor")
    potencia_kw: float = Field(..., ge=0.1, description="Potência em kW")
    recursos: Optional[str] = Field(default="", description="Recursos adicionais (ex: AFCI)")


class SistemaModel(BaseModel):
    """Dados do sistema fotovoltaico"""
    modulos: ModulosModel
    inversores: InversoresModel


class InvestimentoModel(BaseModel):
    """Dados de investimento"""
    kit_fotovoltaico: float = Field(..., ge=0, description="Valor do kit fotovoltaico")
    mao_de_obra: float = Field(..., ge=0, description="Valor da mão de obra, projeto e periféricos")


class ProducaoMensalModel(BaseModel):
    """Dados de produção mensal"""
    mes: Union[int, str] = Field(..., description="Mês (1-12 ou 'média')")
    geracao_total: float = Field(..., ge=0, description="Geração total estimada em kWh")


class RetornoInvestimentoModel(BaseModel):
    """Dados de retorno do investimento por ano"""
    ano: int = Field(..., ge=1, le=25, description="Ano (1-25)")
    saldo: float = Field(..., description="Saldo acumulado")
    economia_mensal: float = Field(..., ge=0, description="Economia média mensal")
    economia_anual: float = Field(..., ge=0, description="Economia anual")


class PropostaRequest(BaseModel):
    """Request completo para geração de proposta"""
    cliente: ClienteModel
    sistema: SistemaModel
    investimento: InvestimentoModel
    producao_mensal: List[ProducaoMensalModel]
    retorno_investimento: List[RetornoInvestimentoModel]
    
    class Config:
        json_schema_extra = {
            "example": {
                "cliente": {
                    "nome": "Paroquia Santo Antônio de Pádua"
                },
                "sistema": {
                    "modulos": {
                        "quantidade": 60,
                        "marca": "Honor Solar",
                        "potencia_w": 620,
                        "tipo": "Mono"
                    },
                    "inversores": {
                        "quantidade": 2,
                        "marca": "SOFAR",
                        "potencia_kw": 20.0,
                        "recursos": "AFCI"
                    }
                },
                "investimento": {
                    "kit_fotovoltaico": 46028.29,
                    "mao_de_obra": 30000.00
                },
                "producao_mensal": [
                    {"mes": 1, "geracao_total": 1548},
                    {"mes": 2, "geracao_total": 1458},
                    {"mes": "média", "geracao_total": 1460}
                ],
                "retorno_investimento": [
                    {"ano": 1, "saldo": -76028.29, "economia_mensal": 1460, "economia_anual": 17520},
                    {"ano": 2, "saldo": -58508.29, "economia_mensal": 1386.03, "economia_anual": 16632.42}
                ]
            }
        }


class PropostaResponse(BaseModel):
    """Response da geração de proposta"""
    success: bool
    message: str
    pdf_filename: Optional[str] = None
    pdf_url: Optional[str] = None
    pdf_base64: Optional[str] = None
    dados_calculados: Optional[Dict[str, Any]] = None
