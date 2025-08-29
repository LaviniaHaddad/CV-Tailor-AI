# src/app.py
import json
import pdfkit
from jinja2 import Template
from nlp_processor import NLPProcessor
from pdf_word_extractor import CurriculoExtractor
import os

def main():
    # 1. Extrai dados automaticamente dos currículos
    print("📂 Extraindo informações dos seus currículos...")
    extractor = CurriculoExtractor()

    if not os.path.exists("curriculos_originais"):
        os.makedirs("curriculos_originais")
        print("⚠️  Por favor, coloque seus currículos na pasta 'curriculos_originais' e rode novamente.")
        return

    dados = extractor.processar_pasta_curriculos("curriculos_originais")

    # 2. Pede a descrição da vaga
    print("\n📝 Cole a descrição da vaga abaixo (Ctrl+Z + Enter para finalizar):")
    descricao_vaga = ""
    try:
        while True:
            linha = input()
            descricao_vaga += linha + "\n"
    except EOFError:
        pass

    # 3. Personaliza com base na vaga
    processor = NLPProcessor()
    palavras_chave = processor.extrair_palavras_chave(descricao_vaga)
    print(f"🎯 Palavras-chave identificadas: {palavras_chave}")

    # 4. Prepara dados para o template
    perfil = {
        "nome": "Lavinia Haddad",
        "contato": {
            "email": "laviniahaddad@hotmail.com",
            "linkedin": "linkedin.com/in/lavinia-haddad",
            "github": "github.com/LaviniaHaddad"
        },
        "resumo": "Analista de Dados com experiência em transformar dados complexos em insights estratégicos.",
        "habilidades_tecnicas": dados["habilidades"] if "habilidades" in dados else [],
        "experiencias": [{"cargo": exp, "realizacoes": [exp]} for exp in dados.get("experiencias", [])[:5]],
        "projetos": [{"nome": proj, "descricao": proj} for proj in dados.get("projetos", [])[:3]]
    }

    # 5. Carrega o template HTML
    with open('templates/base_template.html', 'r', encoding='utf-8') as f:
        template_str = f.read()

    template = Template(template_str)
    html_output = template.render(**perfil)

    # 6. Gera o HTML (vamos focar nisso primeiro)
    try:
        # Garante que a pasta outputs existe
        if not os.path.exists("outputs"):
            os.makedirs("outputs")
        
        # Salva o HTML
        with open('outputs/curriculo_personalizado.html', 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        print("✅ Currículo HTML gerado com sucesso: outputs/curriculo_personalizado.html")
        print("📋 Abra este arquivo no navegador para visualizar")
        
    except Exception as e:
        print(f"❌ Erro ao gerar HTML: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()