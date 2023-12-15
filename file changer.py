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

    full_name = re.search("n?ome:\s*(.+?)(?:(?:(?:\\n)*i?RG:)|(?:\smatr[ií]cula:))", text, re.IGNORECASE)

    if full_name is None:
        return None

    full_name = full_name.group(1)
    full_name = full_name.replace(":", "").replace("_", "").replace("|", "").replace('[', "").replace("]", "").replace("*", "")
    return full_name

def convert_first_page_to_img(file_path, save_path, pdf_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    file_name = file_name + '.pdf'
    
    images_from_path = convert_from_path(file_path, fmt="jpeg")
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
