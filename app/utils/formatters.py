"""
Utilitários de Formatação
Funções para formatação de valores no padrão brasileiro
"""

from typing import Union


def formatar_moeda_br(valor: Union[int, float]) -> str:
    """
    Formata um valor numérico como moeda brasileira (R$).
    
    Args:
        valor: Valor numérico a ser formatado
        
    Returns:
        String formatada como "R$ 1.234,56"
        
    Examples:
        >>> formatar_moeda_br(1234.56)
        'R$ 1.234,56'
        >>> formatar_moeda_br(1000000)
        'R$ 1.000.000,00'
    """
    # Formatar com 2 casas decimais
    valor_str = f"{valor:,.2f}"
    
    # Trocar separadores (padrão US -> BR)
    # Primeiro substitui vírgula por placeholder
    valor_str = valor_str.replace(",", "X")
    # Depois substitui ponto por vírgula
    valor_str = valor_str.replace(".", ",")
    # Por fim substitui placeholder por ponto
    valor_str = valor_str.replace("X", ".")
    
    return f"R$ {valor_str}"


def formatar_numero_br(valor: Union[int, float], casas_decimais: int = 2) -> str:
    """
    Formata um número no padrão brasileiro (sem símbolo de moeda).
    
    Args:
        valor: Valor numérico a ser formatado
        casas_decimais: Número de casas decimais (padrão: 2)
        
    Returns:
        String formatada como "1.234,56"
        
    Examples:
        >>> formatar_numero_br(1234.56)
        '1.234,56'
        >>> formatar_numero_br(1000, casas_decimais=0)
        '1.000'
    """
    # Formatar com casas decimais especificadas
    formato = f"{{:,.{casas_decimais}f}}"
    valor_str = formato.format(valor)
    
    # Trocar separadores (padrão US -> BR)
    valor_str = valor_str.replace(",", "X")
    valor_str = valor_str.replace(".", ",")
    valor_str = valor_str.replace("X", ".")
    
    return valor_str


def formatar_potencia_kw(valor: float) -> str:
    """
    Formata um valor de potência em kW.
    
    Args:
        valor: Potência em kW
        
    Returns:
        String formatada como "20,00 kW"
    """
    return f"{formatar_numero_br(valor)} kW"


def formatar_potencia_kwp(valor: float) -> str:
    """
    Formata um valor de potência em kWp.
    
    Args:
        valor: Potência em kWp
        
    Returns:
        String formatada como "37,20 kWp"
    """
    return f"{formatar_numero_br(valor)} kWp"


def formatar_energia_kwh(valor: float) -> str:
    """
    Formata um valor de energia em kWh.
    
    Args:
        valor: Energia em kWh
        
    Returns:
        String formatada como "4.560 kWh"
    """
    return f"{formatar_numero_br(valor, casas_decimais=0)} kWh"


def ordinal(numero: int) -> str:
    """
    Retorna o número ordinal em português.
    
    Args:
        numero: Número inteiro
        
    Returns:
        String com ordinal, ex: "1º", "2º", "5º"
    """
    return f"{numero}º"
