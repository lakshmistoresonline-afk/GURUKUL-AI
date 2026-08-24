import pdfplumber
import sys

def inspect(path):
    with pdfplumber.open(path) as pdf:
        print(f"Pages: {len(pdf.pages)}")
        first_page = pdf.pages[0].extract_text()
        print("--- FIRST PAGE ---")
        print(first_page)

if __name__ == "__main__":
    inspect(sys.argv[1])
