"""
Modelos Pydantic para validação de dados da API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any


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
    """Request para geração de proposta - estrutura plana"""
    # Cliente
    nome: str = Field(..., description="Nome do cliente")
    
    # Módulos
    modulos_quantidade: int = Field(..., ge=1, description="Quantidade de módulos")
    especificacoes_modulo: str = Field(..., description="Marca e especificações do módulo")
    modulos_potencia_w: Optional[int] = Field(default=620, description="Potência em Watts")
    modulos_tipo: Optional[str] = Field(default="Mono", description="Tipo do módulo")
    
    # Inversores
    inversores_quantidade: int = Field(..., ge=1, description="Quantidade de inversores")
    especificacoes_inversores: str = Field(..., description="Marca e especificações do inversor")
    inversores_potencia_kw: Optional[float] = Field(default=20.0, description="Potência em kW")
    inversores_recursos: Optional[str] = Field(default="AFCI", description="Recursos adicionais")
    
    # Investimento
    investimento_kit_fotovoltaico: float = Field(..., ge=0, description="Valor do kit")
    investimento_mao_de_obra: float = Field(..., ge=0, description="Valor da mão de obra")
    
    # Dados calculados
    producao_mensal: List[ProducaoMensalModel]
    retorno_investimento: List[RetornoInvestimentoModel]


class PropostaResponse(BaseModel):
    """Response da geração de proposta"""
    success: bool
    message: str
    pdf_filename: Optional[str] = None
    pdf_url: Optional[str] = None
    pdf_base64: Optional[str] = None
    dados_calculados: Optional[Dict[str, Any]] = None
