import json
import pdfkit
from jinja2 import Template

# Configura o caminho para o wkhtmltopdf
caminho_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=caminho_wkhtmltopdf)

# 1. Carrega seu perfil
with open('data/profile.json', 'r', encoding='utf-8') as f:  # Alterado
    perfil = json.load(f)

# 2. Carrega o template HTML
with open('templates/base_template.html', 'r', encoding='utf-8') as f:  # Alterado
    template_str = f.read()

template = Template(template_str)
html_output = template.render(**perfil)

# 3. Salva HTML temporário (opcional, para debug)
with open('temp_curriculo.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

# 4. Gera o PDF
try:
    pdfkit.from_string(html_output, 'curriculo_gerado.pdf', configuration=config)
    print("✅ Currículo gerado com sucesso: curriculo_gerado.pdf")
except Exception as e:
    print(f"❌ Erro ao gerar PDF: {e}")
    print("Verifique se o wkhtmltopdf está instalado corretamente no caminho especificado.")