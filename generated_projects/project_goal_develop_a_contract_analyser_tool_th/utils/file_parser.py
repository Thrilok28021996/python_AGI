import docx2txt
import PyPDF2

def parse_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        content = ""
        for page in reader.pages:
            content += page.extract_text()
    return content

def parse_docx(file_path):
    return docx2txt.process(file_path)