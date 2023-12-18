import os
import re
from pdf2image import convert_from_path
import tempfile
from PIL import Image, ImageEnhance
import pytesseract

def getStudentName(jpg_path):
    image = Image.open(jpg_path)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)

    image = image.convert('L')
    threshold = 90

    text = pytesseract.image_to_string(image)

    student_name_regex = r'n?o?me:\s*(.+?)(?:(?:(?:\n)*i?RG\b)|(?:\s[lm]?atr[ií]?cula))'

    likely_student_name = re.search(student_name_regex, text, re.IGNORECASE)
    if likely_student_name is None:
        print("ERRO: Não foi possível extrair o nome do  estudante...")
        return None

    sanitize_name = lambda name: re.sub(r'[^\w\s]|\s{2,}|[\d_]', '', name).upper().strip()
    return sanitize_name(likely_student_name.group(1))

def convert_first_page_to_img(file_path, save_path, pdf_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    file_name = file_name + '.pdf'
    
    images_from_path = convert_from_path(file_path, 
    fmt="jpeg",
    grayscale=True,
    jpegopt={
        "quality": 100
    },
    last_page = 1,
    )

    image_path = os.path.join(save_path, f'{file_name}_page1.jpg')
    images_from_path[0].save(image_path, 'JPEG')
    
    return image_path

root_dir = os.getcwd()
folder = input('SELECIONE UMA PASTA:  ')
save_path = os.path.join(folder, 'saved')
os.makedirs(save_path, exist_ok=True)
pdf_path = root_dir + '/' + folder
pdf_list = os.scandir(pdf_path)

success = 0
failed = 0
count_names = 0

for file in pdf_list:
    if file.is_file() and file.name.lower().endswith('.pdf'):
        print('Convertendo arquivo', file.path)
        img_path = convert_first_page_to_img(file.path, save_path, pdf_path)
        student_name = getStudentName(img_path)
        if student_name is not None:
            print(f'Nome extraido do pdf: {student_name}')
            count_names += 1
            os.rename(file.path, pdf_path + '/' + student_name + str(count_names) + '.pdf')
            success += 1
        else:
            print('Falha ao extrair nome do pdf')
            failed += 1

if success > 0:
    print(f'Foram renomeados {success} arquivos')
if failed > 0:
    print(f'falha ao extrair o nome de {failed} arquivos')
