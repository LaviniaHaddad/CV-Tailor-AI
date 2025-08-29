# CV Tailor AI 🤖

**Gerador Inteligente de Currículos Personalizados com IA**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/ML-NLP%2FTF--IDF-orange)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Status-Funcional-green)](https://github.com/LaviniaHaddad/CV-Tailor-AI)

## 🎯 Sobre o Projeto

O **CV Tailor AI** é uma ferramenta inteligente que usa processamento de linguagem natural (NLP) para personalizar automaticamente currículos com base na descrição de vagas específicas.

### ✨ Funcionalidades Atuais

- ✅ **Extração automática** de informações de múltiplos currículos (PDF/DOCX)  
- ✅ **Análise NLP** de descrições de vagas usando TF-IDF  
- ✅ **Identificação automática** de palavras-chave relevantes  
- ✅ **Geração de currículos personalizados** em HTML/PDF  
- ✅ **Destaque automático** de habilidades e experiências relevantes  

## 🛠️ Tecnologias Utilizadas

- **Python** - Linguagem principal  
- **pdfplumber** & **python-docx** - Extração de texto de PDFs e Word  
- **scikit-learn** - TF-IDF para NLP e extração de palavras-chave  
- **spaCy** - Processamento de linguagem natural em português  
- **Jinja2** - Templates HTML para currículos  
- **pdfkit/wkhtmltopdf** - Geração de PDFs  

## 📦 Instalação

    # Clone o repositório
    git clone https://github.com/LaviniaHaddad/CV-Tailor-AI.git
    cd CV-Tailor-AI

    # Instale as dependências
    pip install -r requirements.txt

    # Instale o wkhtmltopdf (para geração de PDFs)
    # Download: https://wkhtmltopdf.org/downloads.html

    # Instale o modelo de NLP em português
    python -m spacy download pt_core_news_sm

## 🚀 Como Usar

Coloque seus currículos na pasta `curriculos_originais/`

    # Execute o sistema:
    python src/app.py

Cole a descrição da vaga quando solicitado.  
Visualize o currículo personalizado em `outputs/curriculo_personalizado.html`

## 🔧 Processo de Desenvolvimento

### 📋 Desafios Enfrentados

#### ✅ Extração de Texto de PDFs
- **Problema:** PDFs com layout complexo  
- **Solução:** Uso combinado de `pdfplumber` e lógica de parsing personalizada

#### ✅ Processamento de Linguagem Natural em Português
- **Problema:** Modelos NLP em português limitados  
- **Solução:** `spaCy` + `TF-IDF` com tuning para termos técnicos

#### ✅ Identificação de Seções Automática
- **Problema:** Diferentes formatos de currículo  
- **Solução:** Algoritmo de detecção baseado em palavras-chave

#### ✅ Geração de PDF com Formatação
- **Problema:** Compatibilidade cross-platform  
- **Solução:** `wkhtmltopdf` + templates HTML flexíveis

## 🎯 Melhorias Implementadas

- Sistema de extração automática de múltiplos currículos  
- Algoritmo TF-IDF personalizado para termos técnicos  
- Destaque visual de palavras-chave relevantes  
- Organização inteligente por relevância para a vaga  
- Interface de linha de comando intuitiva

## 📅 Próximas Melhorias

- Interface web com Streamlit  
- Web scraping automático de vagas do LinkedIn  
- Integração com GPT-4 para resumos personalizados  
- Sistema de scoring de adequação à vaga  
- Exportação para múltiplos formatos (PDF, DOCX, TXT)

## 🏗️ Estrutura do Projeto

    CV-Tailor-AI/
    ├── src/
    │   ├── app.py                 # Aplicação principal
    │   ├── nlp_processor.py       # Processamento NLP
    │   └── pdf_word_extractor.py  # Extração de textos
    ├── data/
    │   ├── perfil_manual.json     # Dados manuais (alternativo)
    │   └── mapeamento_campos.json # Configuração de campos
    ├── templates/
    │   └── base_template.html     # Template do currículo
    ├── curriculos_originais/      # Seus currículos de entrada
    ├── outputs/                   # Currículos gerados
    └── requirements.txt           # Dependências
