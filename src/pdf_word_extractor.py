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
        """Extrai seções automaticamente do texto do currículo com lógica melhorada"""
        secoes = {
            "contato": [],
            "resumo": [],
            "experiencias": [],
            "educacao": [],
            "habilidades": [],
            "projetos": [],
            "idiomas": []
        }
        
        linhas = texto.split('\n')
        secao_atual = None
        
        for linha in linhas:
            linha = linha.strip()
            if not linha or len(linha) < 2:
                continue
            
            linha_lower = linha.lower()
            
            # Detecta seções pelos cabeçalhos
            for secao, palavras_chave in {
                "contato": ["email", "telefone", "linkedin", "github", "celular"],
                "resumo": ["resumo", "objetivo", "about", "summary"],
                "experiencias": ["experiência", "experiencia", "profissional", "empregos"],
                "educacao": ["educação", "educacao", "formação", "formacao", "acadêmico"],
                "habilidades": ["habilidades", "competências", "skills", "tecnologias"],
                "projetos": ["projetos", "portfólio", "portfolio"],
                "idiomas": ["idiomas", "línguas", "linguas", "inglês", "espanhol"]
            }.items():
                if any(palavra in linha_lower for palavra in palavras_chave):
                    secao_atual = secao
                    break
            
            # Se não é um cabeçalho de seção, adiciona ao conteúdo
            if secao_atual and len(linha) > 5:  # Ignora linhas muito curtas
                # Filtra linhas que são provavelmente conteúdo válido
                if not any(linha_lower.startswith(prefix) for prefix in ['página', 'page', 'http', 'www.']):
                    if secao_atual not in secoes:
                        secoes[secao_atual] = []
                    secoes[secao_atual].append(linha)
        
        return secoes 
    
    def processar_pasta_curriculos(self, pasta_curriculos):
        """Processa todos os currículos de uma pasta"""
        todos_dados = {
            "contato": [],
            "resumo": [],
            "experiencias": [],
            "educacao": [],
            "habilidades": [],
            "projetos": [],
            "idiomas": []
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
                    if secao in todos_dados:  # Só adiciona se a chave existir
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