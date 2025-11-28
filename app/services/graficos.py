"""
Serviço de Geração de Gráficos
Gera os gráficos de produção de energia e tabela de retorno do investimento
"""

import matplotlib
matplotlib.use('Agg')  # Backend não-interativo

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import List
import os
import uuid

from app.models.proposta import ProducaoMensalModel, RetornoInvestimentoModel
from app.utils.formatters import formatar_moeda_br, formatar_numero_br


class GraficoService:
    """Serviço para geração de gráficos da proposta"""
    
    # Cores padrão Level5
    COR_AZUL_ESCURO = '#2C3E50'
    COR_TEAL = '#16A085'
    COR_LARANJA = '#E67E22'
    COR_CINZA = '#7F8C8D'
    COR_FUNDO = '#FFFFFF'
    
    def gerar_grafico_producao(
        self,
        dados_producao: List[ProducaoMensalModel],
        quantidade_modulos: int,
        output_dir: str
    ) -> str:
        """
        Gera o gráfico de barras de produção de energia mensal.
        
        Args:
            dados_producao: Lista com dados de produção mensal
            quantidade_modulos: Quantidade de módulos para calcular geração por placa
            output_dir: Diretório para salvar o gráfico
            
        Returns:
            Caminho do arquivo PNG gerado
        """
        # Preparar dados
        meses = []
        geracao_total = []
        geracao_por_placa = []
        
        for item in dados_producao:
            # Converter mês para label
            if isinstance(item.mes, int):
                meses.append(str(item.mes))
            else:
                meses.append('MÉDIA')
            
            geracao_total.append(item.geracao_total)
            geracao_por_placa.append(round(item.geracao_total / quantidade_modulos, 0))
        
        # Configurar figura
        fig, ax = plt.subplots(figsize=(12, 6), dpi=150)
        fig.patch.set_facecolor(self.COR_FUNDO)
        ax.set_facecolor(self.COR_FUNDO)
        
        # Posições das barras
        x = np.arange(len(meses))
        width = 0.35
        
        # Criar barras
        bars1 = ax.bar(x - width/2, geracao_por_placa, width, 
                       label='geração por placa', color=self.COR_AZUL_ESCURO,
                       edgecolor='white', linewidth=0.5)
        bars2 = ax.bar(x + width/2, geracao_total, width,
                       label='geração total estimada', color=self.COR_TEAL,
                       edgecolor='white', linewidth=0.5)
        
        # Adicionar rótulos nas barras
        def add_labels(bars, fontsize=7):
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{int(height)}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom',
                           fontsize=fontsize, fontweight='bold',
                           color=self.COR_AZUL_ESCURO)
        
        add_labels(bars1, fontsize=7)
        add_labels(bars2, fontsize=7)
        
        # Configurar eixos
        ax.set_xlabel('MÊS', fontsize=10, fontweight='bold', color=self.COR_AZUL_ESCURO)
        ax.set_ylabel('GERAÇÃO', fontsize=10, fontweight='bold', color=self.COR_AZUL_ESCURO)
        ax.set_xticks(x)
        ax.set_xticklabels(meses, fontsize=9)
        
        # Título
        ax.set_title('PRODUÇÃO DE ENERGIA', fontsize=14, fontweight='bold', 
                    color=self.COR_AZUL_ESCURO, pad=20)
        
        # Legenda
        legend = ax.legend(loc='upper right', frameon=True, fontsize=9)
        legend.get_frame().set_facecolor(self.COR_FUNDO)
        legend.get_frame().set_edgecolor(self.COR_CINZA)
        
        # Grid suave
        ax.yaxis.grid(True, linestyle='--', alpha=0.3, color=self.COR_CINZA)
        ax.set_axisbelow(True)
        
        # Remover bordas
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(self.COR_CINZA)
        ax.spines['bottom'].set_color(self.COR_CINZA)
        
        # Ajustar layout
        plt.tight_layout()
        
        # Salvar
        filename = f"grafico_producao_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight', 
                   facecolor=self.COR_FUNDO, edgecolor='none')
        plt.close(fig)
        
        return filepath
    
    def gerar_tabela_retorno(
        self,
        dados_retorno: List[RetornoInvestimentoModel],
        output_dir: str
    ) -> str:
        """
        Gera a tabela de retorno do investimento como imagem.
        
        Args:
            dados_retorno: Lista com dados de retorno por ano
            output_dir: Diretório para salvar a imagem
            
        Returns:
            Caminho do arquivo PNG gerado
        """
        # Preparar dados para a tabela
        dados_tabela = []
        for item in dados_retorno:
            # Formatar saldo com sinal
            if item.saldo < 0:
                saldo_str = f"-R$  {formatar_numero_br(abs(item.saldo))}"
            else:
                saldo_str = f"R$  {formatar_numero_br(item.saldo)}"
            
            dados_tabela.append([
                str(item.ano),
                saldo_str,
                f"R$  {formatar_numero_br(item.economia_mensal)}",
                f"R$  {formatar_numero_br(item.economia_anual)}"
            ])
        
        # Configurar figura
        fig, ax = plt.subplots(figsize=(10, 12), dpi=150)
        fig.patch.set_facecolor(self.COR_FUNDO)
        ax.set_facecolor(self.COR_FUNDO)
        ax.axis('off')
        
        # Cabeçalhos
        headers = ['ANO', 'SALDO', 'ECONOMIA MÉDIA MENSAL', 'ECONOMIA ANUAL']
        
        # Cores das células
        cell_colors = []
        for i, row in enumerate(dados_tabela):
            if i == 0:  # Primeira linha após header
                cell_colors.append([self.COR_FUNDO] * 4)
            else:
                cell_colors.append([self.COR_FUNDO] * 4)
        
        # Criar tabela
        table = ax.table(
            cellText=dados_tabela,
            colLabels=headers,
            cellLoc='center',
            loc='center',
            colColours=[self.COR_CINZA] * 4,
            cellColours=cell_colors
        )
        
        # Estilizar tabela
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1.2, 1.5)
        
        # Estilizar células
        for (row, col), cell in table.get_celld().items():
            cell.set_edgecolor(self.COR_CINZA)
            cell.set_linewidth(0.5)
            
            if row == 0:  # Header
                cell.set_text_props(fontweight='bold', color='white')
                cell.set_facecolor(self.COR_AZUL_ESCURO)
            else:
                # Alternar cores das linhas
                if row % 2 == 0:
                    cell.set_facecolor('#F8F9FA')
                else:
                    cell.set_facecolor(self.COR_FUNDO)
                
                # Destacar valores negativos/positivos na coluna SALDO
                if col == 1:  # Coluna SALDO
                    cell_text = dados_tabela[row-1][1]
                    if cell_text.startswith('-'):
                        cell.set_text_props(color='#C0392B')  # Vermelho para negativo
                    else:
                        cell.set_text_props(color=self.COR_TEAL)  # Verde para positivo
        
        # Ajustar largura das colunas
        table.auto_set_column_width([0, 1, 2, 3])
        
        # Salvar
        filename = f"tabela_retorno_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight',
                   facecolor=self.COR_FUNDO, edgecolor='none',
                   pad_inches=0.1)
        plt.close(fig)
        
        return filepath
