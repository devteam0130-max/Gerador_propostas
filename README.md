# 🔆 API Gerador de Propostas Solar

API para geração automática de propostas comerciais em PDF para sistemas fotovoltaicos.

**Empresa:** Level5 Engenharia Elétrica  
**Porta:** 3493

---

## 📋 Funcionalidades

- ✅ Geração de PDF personalizado com dados do cliente
- ✅ Gráfico de produção de energia mensal
- ✅ Tabela de retorno do investimento (25 anos)
- ✅ Cálculo automático de payback e economia
- ✅ Formatação brasileira (R$, vírgula decimal)
- ✅ API RESTful com documentação Swagger

---

## 🚀 Deploy no EasyPanel

### 1. Criar Repositório no GitHub

```bash
git init
git add .
git commit -m "Initial commit - API Propostas Solar"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/proposta-solar-api.git
git push -u origin main
```

### 2. Configurar no EasyPanel

1. Acesse seu EasyPanel
2. Clique em **"Create Service"** → **"App"**
3. Conecte ao repositório GitHub
4. Configure:
   - **Build Method:** Dockerfile
   - **Port:** 3493
   - **Domain:** (opcional) seu-dominio.com

### 3. Variáveis de Ambiente (opcional)

```
TZ=America/Sao_Paulo
```

---

## 🔌 Endpoints

### Health Check
```
GET /api/v1/health
```

### Gerar Proposta
```
POST /api/v1/proposta/gerar
Content-Type: application/json
```

### Download PDF
```
GET /api/v1/download/{filename}
```

### Preview Gráfico
```
POST /api/v1/graficos/producao/preview
```

---

## 📦 Payload de Exemplo

```json
{
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
    {"mes": 3, "geracao_total": 1426},
    {"mes": 4, "geracao_total": 1390},
    {"mes": 5, "geracao_total": 1302},
    {"mes": 6, "geracao_total": 1268},
    {"mes": 7, "geracao_total": 1232},
    {"mes": 8, "geracao_total": 1302},
    {"mes": 9, "geracao_total": 1354},
    {"mes": 10, "geracao_total": 1408},
    {"mes": 11, "geracao_total": 1496},
    {"mes": 12, "geracao_total": 1528},
    {"mes": "média", "geracao_total": 1460}
  ],
  "retorno_investimento": [
    {"ano": 1, "saldo": -76028.29, "economia_mensal": 1460.00, "economia_anual": 17520.00},
    {"ano": 2, "saldo": -58508.29, "economia_mensal": 1386.03, "economia_anual": 16632.42},
    {"ano": 3, "saldo": -41875.87, "economia_mensal": 1376.33, "economia_anual": 16515.99},
    {"ano": 4, "saldo": -25359.88, "economia_mensal": 1366.70, "economia_anual": 16400.38},
    {"ano": 5, "saldo": -8959.50, "economia_mensal": 1526.59, "economia_anual": 18319.06},
    {"ano": 6, "saldo": 9359.56, "economia_mensal": 1576.54, "economia_anual": 18918.46},
    {"ano": 7, "saldo": 28278.02, "economia_mensal": 1628.12, "economia_anual": 19537.47},
    {"ano": 8, "saldo": 47815.49, "economia_mensal": 1681.39, "economia_anual": 20176.74},
    {"ano": 9, "saldo": 67992.23, "economia_mensal": 1736.41, "economia_anual": 20836.92},
    {"ano": 10, "saldo": 88829.15, "economia_mensal": 1793.23, "economia_anual": 21518.70},
    {"ano": 11, "saldo": 110347.85, "economia_mensal": 1851.90, "economia_anual": 22222.80},
    {"ano": 12, "saldo": 132570.65, "economia_mensal": 1912.49, "economia_anual": 22949.93},
    {"ano": 13, "saldo": 155520.57, "economia_mensal": 1975.07, "economia_anual": 23700.85},
    {"ano": 14, "saldo": 179221.42, "economia_mensal": 2039.69, "economia_anual": 24476.34},
    {"ano": 15, "saldo": 203697.76, "economia_mensal": 2106.43, "economia_anual": 25277.21},
    {"ano": 16, "saldo": 228974.97, "economia_mensal": 2175.36, "economia_anual": 26104.28},
    {"ano": 17, "saldo": 255079.24, "economia_mensal": 2246.53, "economia_anual": 26958.41},
    {"ano": 18, "saldo": 282037.65, "economia_mensal": 2320.04, "economia_anual": 27840.49},
    {"ano": 19, "saldo": 309878.13, "economia_mensal": 2395.95, "economia_anual": 28751.43},
    {"ano": 20, "saldo": 338629.56, "economia_mensal": 2474.35, "economia_anual": 29692.17},
    {"ano": 21, "saldo": 368321.74, "economia_mensal": 2555.31, "economia_anual": 30663.70},
    {"ano": 22, "saldo": 398985.44, "economia_mensal": 2638.92, "economia_anual": 31667.02},
    {"ano": 23, "saldo": 430652.45, "economia_mensal": 2725.26, "economia_anual": 32703.16},
    {"ano": 24, "saldo": 463355.62, "economia_mensal": 2814.43, "economia_anual": 33773.21},
    {"ano": 25, "saldo": 497128.83, "economia_mensal": 2906.52, "economia_anual": 34878.27}
  ]
}
```

---

## 📤 Response

```json
{
  "success": true,
  "message": "Proposta gerada com sucesso",
  "pdf_filename": "proposta_paroquia_santo_antonio_de_padua_abc12345.pdf",
  "pdf_url": "/api/v1/download/proposta_paroquia_santo_antonio_de_padua_abc12345.pdf",
  "pdf_base64": "JVBERi0xLjQK...",
  "dados_calculados": {
    "investimento_total": 76028.29,
    "ano_payback": 6,
    "valor_payback": 9359.56,
    "economia_25_anos": 497128.83
  }
}
```

---

## 🔧 Integração com N8N

### Workflow Sugerido

```
[Google Sheets Trigger] 
    ↓
[Formatar Dados (Function Node)]
    ↓
[HTTP Request POST para API]
    ↓
[Processar Response / Enviar PDF]
```

### Nó HTTP Request

```json
{
  "method": "POST",
  "url": "http://SEU_SERVIDOR:3493/api/v1/proposta/gerar",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "={{ JSON.stringify($json) }}"
}
```

---

## 🖥️ Desenvolvimento Local

### Com Docker

```bash
docker-compose up --build
```

### Sem Docker

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar aplicação
uvicorn app.main:app --host 0.0.0.0 --port 3493 --reload
```

### Acessar Documentação

- Swagger UI: http://localhost:3493/docs
- ReDoc: http://localhost:3493/redoc

---

## 📁 Estrutura do Projeto

```
proposta-solar-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── proposta.py         # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── graficos.py         # Geração de gráficos
│   │   ├── pdf_generator.py    # Geração do PDF
│   │   └── calculos.py         # Cálculos auxiliares
│   └── utils/
│       ├── __init__.py
│       └── formatters.py       # Formatação BR
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 📊 Variáveis Dinâmicas no PDF

| Página | Campo | Fonte |
|--------|-------|-------|
| 1 | Nome do Cliente | `cliente.nome` |
| 2 | Descrição Módulos | `sistema.modulos.*` |
| 2 | Descrição Inversores | `sistema.inversores.*` |
| 3 | Kit Fotovoltaico | `investimento.kit_fotovoltaico` |
| 3 | Mão de Obra | `investimento.mao_de_obra` |
| 3 | **Investimento Total** | Calculado |
| 4 | Gráfico Produção | `producao_mensal[]` |
| 4 | Tabela Retorno | `retorno_investimento[]` |
| 4 | Ano do Payback | Calculado |
| 4 | Economia 25 anos | Calculado |

---

## 📝 Licença

Proprietário - Level5 Engenharia Elétrica

---

## 🤝 Suporte

Para dúvidas ou sugestões, entre em contato com a equipe de desenvolvimento.
