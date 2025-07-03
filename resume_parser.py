import pdfplumber
import docx

def extract_text(filepath):
    if filepath.endswith('.pdf'):
        with pdfplumber.open(filepath) as pdf:
            return "\n".join(page.extract_text() or '' for page in pdf.pages)
    elif filepath.endswith('.docx'):
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    elif filepath.endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""
