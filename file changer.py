import os
from pdf2image import convert_from_path
import tempfile
from PIL import Image
import pytesseract

def getStudentName(jpg_path):
    
    text = pytesseract.image_to_string(Image.open(jpg_path))
    keyword = 'Nome'
    pos = text.find('Nome')
    
    startName = pos + len(keyword)
    endName = text.find('RG', startName)

    fullName = text[startName:endName].strip()
        
    return fullName

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
pdf_path = root_dir + '\\' + folder
pdf_list = os.scandir(pdf_path)

for file in pdf_list:
    if file.is_file() and file.name.lower().endswith('.pdf'):
        print('Convertendo arquivo', file.path)
        img_path = convert_first_page_to_img(file.path, save_path, pdf_path)
        student_name = getStudentName(img_path)
        
        os.rename(file.path, pdf_path + '\\' + student_name + '.pdf')
