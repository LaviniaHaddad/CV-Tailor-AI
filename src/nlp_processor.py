# src/nlp_processor.py
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class NLPProcessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=50,
            ngram_range=(1, 2)  # Captura palavras simples e bigramas
        )
    
    def limpar_texto(self, texto):
        """Limpa e padroniza o texto"""
        if not texto:
            return ""
        
        # Remove caracteres especiais, números e converte para minúsculo
        texto_limpo = re.sub(r'[^a-zA-ZÀ-ÿ\s]', ' ', texto.lower())
        # Remove espaços extras
        texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
        return texto_limpo
    
    def extrair_palavras_chave(self, texto, max_keywords=15):
        """Extrai palavras-chave importantes do texto usando TF-IDF"""
        texto_limpo = self.limpar_texto(texto)
        if not texto_limpo or len(texto_limpo.split()) < 3:
            return []
        
        try:
            # Treina o TF-IDF com o texto
            X = self.vectorizer.fit_transform([texto_limpo])
            # Pega as palavras mais importantes
            feature_names = self.vectorizer.get_feature_names_out()
            scores = X.toarray()[0]
            
            # Combina palavras e scores
            palavras_com_scores = list(zip(feature_names, scores))
            # Ordena por score (maior primeiro)
            palavras_com_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Retorna apenas as palavras (sem scores)
            return [palavra for palavra, score in palavras_com_scores[:max_keywords]]
        
        except Exception as e:
            print(f"Erro ao extrair palavras-chave: {e}")
            return []
    
    def calcular_relevancia(self, texto, palavras_chave):
        """Calcula quão relevante é um texto baseado nas palavras-chave"""
        if not palavras_chave or not texto:
            return 0
        
        texto_limpo = self.limpar_texto(texto)
        palavras_texto = texto_limpo.split()
        
        # Conta quantas palavras-chave aparecem no texto
        correspondencias = sum(1 for palavra in palavras_chave if palavra in texto_limpo)
        
        # Calcula score de relevância (0 a 1)
        return min(correspondencias / len(palavras_chave), 1.0) if palavras_chave else 0

# Exemplo de uso para teste
if __name__ == "__main__":
    processor = NLPProcessor()
    
    # Texto de exemplo (descrição de vaga)
    vaga_exemplo = """
    Buscamos Analista de Dados Júnior com conhecimentos em Python, Pandas, 
    Power BI e SQL. Experiência em ETL e análise de dados. Conhecimentos em 
    machine learning são um diferencial.
    """
    
    palavras_chave = processor.extrair_palavras_chave(vaga_exemplo)
    print("Palavras-chave extraídas:", palavras_chave)