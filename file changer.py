import os
import re
from pdf2image import convert_from_path
import pytesseract

def getStudentName(jpeg):
    text = pytesseract.image_to_string(jpeg, lang="por")

    student_name_regex = r'n?o?me:\s*(.+?)(?:(?:(?:\n)*i?RG\b)|(?:\s[lm]?atr[ií]?cula))'

    likely_student_name = re.search(student_name_regex, text, re.IGNORECASE)
    if likely_student_name is None:
        print("ERRO: Não foi possível extrair o nome do  estudante...")
        return None

    sanitize_name = lambda name: re.sub(r'[^\w\s]|\s{2,}|[\d_]', '', name).upper().strip()
    return sanitize_name(likely_student_name.group(1))

def convert_first_page_to_img(pdf_path):
    jpeg = convert_from_path(pdf_path,
    fmt="jpeg",
    grayscale=True,
    jpegopt={
        "quality": 100
    },
    last_page = 1,
    )
    
    return jpeg[0]

folder = input('SELECIONE UMA PASTA: ').strip()

pdfs_list = []
pdfs_dir = os.scandir(folder)

for file in pdfs_dir:
    if file.is_file() and file.name.lower().endswith('.pdf'):
        pdfs_list.append(file.path)
    else:
        print(f"O arquivo {file.path} não é um PDF")

success = 0
failed = 0
count_names = 0
pdf_count = len(pdfs_list)

print(f"\nQuantidade de PDFS encontrados: {pdf_count} \n")

for pdf in pdfs_list:
    print('Convertendo arquivo', pdf)
    jpeg = convert_first_page_to_img(pdf)
    student_name = getStudentName(jpeg)
    if student_name is not None:
        print(f'Nome extraido do pdf: {student_name}')
        count_names += 1
        os.rename(pdf, os.path.join(os.path.dirname(pdf), student_name + str(count_names) + '.pdf'))
        success += 1
    else:
        print('Falha ao extrair nome do pdf')
        failed += 1

if success > 0:
    print(f'Foram renomeados {success} arquivos')
if failed > 0:
    print(f'falha ao extrair o nome de {failed} arquivos')
