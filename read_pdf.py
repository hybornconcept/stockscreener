import pypdf
import sys

def extract_text(pdf_path):
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    pdf_path = r"c:\Users\Franklin\Documents\stockscreener\Warrior Trading - Stock Selection.pdf"
    print(extract_text(pdf_path))
