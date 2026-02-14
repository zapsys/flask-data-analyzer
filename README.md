# 📊 Flask Data Insight Analyzer

Uma aplicação web robusta desenvolvida com Flask para processamento, filtragem e visualização de dados a partir de arquivos PDF, Excel (XLSX/XLS), ODS e CSV. O sistema é otimizado para lidar com grandes volumes de dados (10.000+ registros) e arquivos PDF extensos (200+ páginas) com alta performance.



## 🚀 Funcionalidades

- **Extração Ultra-Rápida:** Utiliza `PyMuPDF` para leitura de PDFs complexos em segundos.
- **Limpeza Inteligente:** Algoritmo de consenso para identificar tabelas reais, remover cabeçalhos repetidos e tratar quebras de linha (`\n`) indesejadas.
- **Interface Estilo Excel:** Filtragem diretamente nos cabeçalhos das colunas e ordenação rápida.
- **Dashboard Interativo:** Gráficos (Pizza/Barras) gerados automaticamente com base nos dados filtrados, organizados em grid responsivo.
- **Persistência de Dados:** Banco de dados SQLite integrado para histórico de uploads.
- **Controle Total:** Sistema de "Pílulas" para mostrar/ocultar colunas e reordenamento via Drag & Drop.
- **Exportação:** Exporte seus dados filtrados de volta para Excel ou CSV.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.9, Flask, Pandas, SQLite.
* **Processamento de PDF:** PyMuPDF (fitz), pdfplumber.
* **Frontend:** Bootstrap 5, DataTables (ColReorder, Buttons), Chart.js.
* **Containerização:** Docker.

## 📦 Estrutura do Projeto

```text
.
├── app.py              # Lógica principal e rotas da API
├── Dockerfile          # Configuração da imagem Docker
├── requirements.txt    # Dependências do Python
├── data.db             # Banco de dados SQLite (gerado automaticamente)
├── uploads/            # Armazenamento físico dos arquivos enviados
└── templates/          # Arquivos HTML (Jinja2)
    ├── index.html      # Dashboard principal (Histórico e Upload)
    └── view.html       # Visualização detalhada e análise
