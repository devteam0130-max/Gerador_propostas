"""
Serviço de Geração de PDF
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak

import os
from typing import Optional

from app.utils.formatters import formatar_moeda_br


class PDFGenerator:
    
    COR_AZUL_ESCURO = HexColor('#2C3E50')
    COR_TEAL = HexColor('#16A085')
    COR_LARANJA = HexColor('#E67E22')
    COR_CINZA = HexColor('#7F8C8D')
    COR_CINZA_CLARO = HexColor('#ECF0F1')
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._criar_estilos_customizados()
    
    def _criar_estilos_customizados(self):
        self.styles.add(ParagraphStyle(
            name='TituloPrincipal',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=self.COR_AZUL_ESCURO,
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='Corpo',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=black,
            alignment=TA_JUSTIFY,
            spaceBefore=5,
            spaceAfter=5,
            leading=14
        ))
        
        self.styles.add(ParagraphStyle(
            name='Cliente',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=self.COR_AZUL_ESCURO,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='Destaque',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.COR_TEAL,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            spaceBefore=10,
            spaceAfter=5
        ))
    
    def gerar_proposta_plana(
        self,
        nome_cliente: str,
        modulos_quantidade: int,
        especificacoes_modulo: str,
        inversores_quantidade: int,
        especificacoes_inversores: str,
        investimento_kit: float,
        investimento_mao_de_obra: float,
        investimento_total: float,
        grafico_producao_path: str,
        tabela_retorno_path: str,
        ano_payback: Optional[int],
        valor_payback: Optional[float],
        economia_25_anos: float,
        output_path: str
    ):
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        # PÁGINA 1 - CAPA
        story.append(Spacer(1, 3*cm))
        story.append(Paragraph("LEVEL5", self.styles['TituloPrincipal']))
        story.append(Paragraph("ENGENHARIA ELÉTRICA", ParagraphStyle(
            name='Subtitulo2',
            fontSize=12,
            textColor=self.COR_LARANJA,
            alignment=TA_CENTER,
            spaceAfter=50
        )))
        story.append(Spacer(1, 2*cm))
        story.append(Paragraph("PROPOSTA", self.styles['TituloPrincipal']))
        story.append(Paragraph("COMERCIAL", self.styles['TituloPrincipal']))
        story.append(Spacer(1, 3*cm))
        story.append(Paragraph("CLIENTE:", self.styles['Cliente']))
        story.append(Paragraph(nome_cliente.upper(), ParagraphStyle(
            name='ClienteNome',
            fontSize=14,
            textColor=self.COR_TEAL,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            spaceBefore=5
        )))
        story.append(PageBreak())
        
        # PÁGINA 2 - QUEM SOMOS + DESCRIÇÃO
        story.append(self._criar_titulo_secao("QUEM SOMOS?"))
        story.append(Paragraph(
            """Somos uma empresa especializada no segmento de engenharia elétrica, com foco no 
            desenvolvimento de projetos elétricos e na instalação de sistemas fotovoltaicos. Desde 2019, 
            temos trabalhado para oferecer soluções eficientes e sustentáveis, sempre com alto padrão de 
            qualidade. Ao longo de nossa trajetória, já realizamos mais de 700 projetos fotovoltaicos, 
            contribuindo para a geração de energia limpa e a redução de custos energéticos de nossos 
            clientes.""",
            self.styles['Corpo']
        ))
        story.append(Spacer(1, 0.5*cm))
        
        story.append(self._criar_titulo_secao("FUNCIONAMENTO DO SISTEMA FOTOVOLTAICO"))
        story.append(Paragraph(
            """O sistema fotovoltaico é composto principalmente por três componentes: painéis solares, inversor e 
            medidor bidirecional. Os painéis captam a energia solar e a convertem em energia elétrica de 
            corrente contínua (CC). Em seguida, o inversor transforma essa corrente contínua em corrente 
            alternada (CA), que pode ser utilizada pelos equipamentos elétricos.""",
            self.styles['Corpo']
        ))
        story.append(Spacer(1, 0.5*cm))
        
        story.append(self._criar_titulo_secao("DESCRIÇÃO DOS ITENS:"))
        story.append(Paragraph(f"• {modulos_quantidade} {especificacoes_modulo}", self.styles['Corpo']))
        story.append(Paragraph(f"• {inversores_quantidade:02d} inversor{'es' if inversores_quantidade > 1 else ''} {especificacoes_inversores}", self.styles['Corpo']))
        story.append(Spacer(1, 0.5*cm))
        
        story.append(self._criar_titulo_secao("GARANTIA"))
        story.append(Paragraph("A garantia do sistema fotovoltaico é composta por:", self.styles['Corpo']))
        garantias = [
            "<b>Módulos Fotovoltaicos:</b> Garantia de desempenho linear de 25 anos e garantia contra defeitos de fabricação de 15 anos.",
            "<b>Inversor:</b> Garantia de 10 anos contra defeitos de fabricação.",
            "<b>Estrutura de Fixação:</b> Garantia contra corrosão e defeitos de fabricação.",
            "<b>Serviço de Instalação:</b> Garantia de 1 ano."
        ]
        for garantia in garantias:
            story.append(Paragraph(f"• {garantia}", self.styles['Corpo']))
        story.append(PageBreak())
        
        # PÁGINA 3 - INVESTIMENTO
        story.append(self._criar_titulo_secao("INVESTIMENTO"))
        dados_investimento = [
            ['KIT FOTOVOLTAICO', formatar_moeda_br(investimento_kit)],
            ['MÃO DE OBRA, PROJETO E PERIFÉRICOS', formatar_moeda_br(investimento_mao_de_obra)],
            ['INVESTIMENTO TOTAL', formatar_moeda_br(investimento_total)]
        ]
        tabela_invest = Table(dados_investimento, colWidths=[10*cm, 5*cm])
        tabela_invest.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), white),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.COR_AZUL_ESCURO),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, self.COR_CINZA),
            ('LINEBELOW', (0, -1), (-1, -1), 2, self.COR_TEAL),
        ]))
        story.append(tabela_invest)
        story.append(Spacer(1, 1*cm))
        
        story.append(self._criar_titulo_secao("FORMAS DE PAGAMENTO"))
        story.append(Paragraph("Oferecemos diversas formas de pagamento:", self.styles['Corpo']))
        pagamentos = [
            "<b>Pagamento à Vista:</b> Desconto especial.",
            "<b>Financiamento Bancário:</b> Até 120 meses.",
            "<b>Pagamento Parcelado:</b> Direto no cartão."
        ]
        for pag in pagamentos:
            story.append(Paragraph(f"• {pag}", self.styles['Corpo']))
        story.append(PageBreak())
        
        # PÁGINA 4 - CUSTO X BENEFÍCIO
        story.append(self._criar_titulo_secao("CUSTO X BENEFÍCIO"))
        story.append(Paragraph("O gráfico abaixo ilustra a produção estimada de energia mês a mês.", self.styles['Corpo']))
        if os.path.exists(grafico_producao_path):
            story.append(Image(grafico_producao_path, width=16*cm, height=8*cm))
        story.append(Spacer(1, 0.5*cm))
        
        story.append(self._criar_titulo_secao("RETORNO DO INVESTIMENTO"))
        if ano_payback and valor_payback:
            story.append(Paragraph(
                f"• <b>Lucro a partir do {ano_payback}º ano:</b> Retorno acumulado de <b>{formatar_moeda_br(valor_payback)}</b>",
                self.styles['Destaque']
            ))
        story.append(Paragraph(
            f"• <b>Retorno em 25 anos:</b> Economia acumulada de <b>{formatar_moeda_br(economia_25_anos)}</b>",
            self.styles['Destaque']
        ))
        story.append(Spacer(1, 0.3*cm))
        if os.path.exists(tabela_retorno_path):
            story.append(Image(tabela_retorno_path, width=16*cm, height=18*cm))
        
        doc.build(story)
    
    def _criar_titulo_secao(self, titulo: str) -> Paragraph:
        return Paragraph(
            f'<font color="{self.COR_TEAL}">{titulo}</font>',
            ParagraphStyle(
                name='SecaoTitulo',
                fontSize=14,
                textColor=self.COR_AZUL_ESCURO,
                alignment=TA_LEFT,
                spaceBefore=15,
                spaceAfter=10,
                fontName='Helvetica-Bold',
                backColor=self.COR_CINZA_CLARO,
                borderPadding=8
            )
        )
