# src/pdf_word_extractor.py
import os
import pdfplumber
from docx import Document
import spacy

class CurriculoExtractor:
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_sm")
    
    def extrair_texto_pdf(self, caminho_pdf):
        """Extrai texto de arquivos PDF"""
        texto = ""
        try:
            with pdfplumber.open(caminho_pdf) as pdf:
                for pagina in pdf.pages:
                    texto += pagina.extract_text() + "\n"
            return texto
        except Exception as e:
            print(f"Erro ao ler PDF {caminho_pdf}: {e}")
            return ""
    
    def extrair_texto_docx(self, caminho_docx):
        """Extrai texto de arquivos Word"""
        texto = ""
        try:
            doc = Document(caminho_docx)
            for paragrafo in doc.paragraphs:
                texto += paragrafo.text + "\n"
            return texto
        except Exception as e:
            print(f"Erro ao ler DOCX {caminho_docx}: {e}")
            return ""
    
    def extrair_secoes_curriculo(self, texto):
        """Extrai seções automaticamente do texto do currículo"""
        secoes = {
            "experiencias": [],
            "educacao": [],
            "habilidades": [],
            "projetos": []
        }
        
        doc = self.nlp(texto)
        
        # Padrões simples para extração (podemos melhorar depois)
        linhas = texto.split('\n')
        current_section = None
        
        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue
            
            # Detecta seções
            lower_line = linha.lower()
            if any(palavra in lower_line for palavra in ["experiência", "experiencia", "empregos", "profissional"]):
                current_section = "experiencias"
            elif any(palavra in lower_line for palavra in ["educação", "educacao", "formação", "acadêmico"]):
                current_section = "educacao"
            elif any(palavra in lower_line for palavra in ["habilidades", "competências", "skills", "tecnologias"]):
                current_section = "habilidades"
            elif any(palavra in lower_line for palavra in ["projetos", "portfólio", "portfolio"]):
                current_section = "projetos"
            
            # Adiciona conteúdo à seção atual
            elif current_section and len(linha) > 10:  # Ignora linhas muito curtas
                if current_section == "habilidades" and any(char.isdigit() for char in linha):
                    continue  # Provavelmente é uma data, não habilidade
                
                secoes[current_section].append(linha)
        
        return secoes
    
    def processar_pasta_curriculos(self, pasta_curriculos):
        """Processa todos os currículos de uma pasta"""
        todos_dados = {
            "experiencias": [],
            "educacao": [],
            "habilidades": [],
            "projetos": []
        }
        
        for arquivo in os.listdir(pasta_curriculos):
            caminho_completo = os.path.join(pasta_curriculos, arquivo)
            
            if arquivo.lower().endswith('.pdf'):
                texto = self.extrair_texto_pdf(caminho_completo)
            elif arquivo.lower().endswith(('.doc', '.docx')):
                texto = self.extrair_texto_docx(caminho_completo)
            else:
                continue
            
            if texto:
                print(f"Processando: {arquivo}")
                secoes = self.extrair_secoes_curriculo(texto)
                
                # Combina os dados de todos os currículos
                for secao, itens in secoes.items():
                    todos_dados[secao].extend(itens)
        
        # Remove duplicatas
        for secao in todos_dados:
            todos_dados[secao] = list(set(todos_dados[secao]))
        
        return todos_dados

# Exemplo de uso
if __name__ == "__main__":
    extractor = CurriculoExtractor()
    
    # Processa todos os currículos na pasta 'curriculos_originais'
    dados_combinados = extractor.processar_pasta_curriculos("curriculos_originais")
    
    print("✅ Dados extraídos:")
    for secao, itens in dados_combinados.items():
        print(f"\n{secao.upper()} ({len(itens)} itens):")
        for item in itens[:5]:  # Mostra apenas os 5 primeiros de cada
            print(f"  - {item}")