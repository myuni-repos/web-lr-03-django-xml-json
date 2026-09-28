import os
import json
import xml.etree.ElementTree as ET
import uuid
from pathlib import Path
from django.conf import settings

STORAGE_DIR = settings.BASE_DIR / 'storage'

def save_grade_to_file(data):
    unique_filename = f"grade_{uuid.uuid4().hex}"
    file_format = data['file_format'] 
    
    file_path = STORAGE_DIR / f"{unique_filename}.{file_format}"

    record = {
        'student_name': data['student_name'],
        'group': data['group'],
        'subject': data['subject'],
        'grade': data['grade'],
        'date': data['date'].strftime('%Y-%m-%d')
    }

    if file_format == 'json':
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=4)
            
    elif file_format == 'xml':
        root = ET.Element("GradeRecord")
        for key, value in record.items():
            child = ET.SubElement(root, key)
            child.text = str(value)

        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)

def get_all_grades():
    if not STORAGE_DIR.exists():
        return []

    grades = []
    
    for file_path in STORAGE_DIR.iterdir():
        if file_path.is_file():
            try:
                if file_path.suffix == '.json':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        data['filename'] = file_path.name
                        grades.append(data)
                        
                elif file_path.suffix == '.xml':
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    # Собираем словарь из тегов XML
                    data = {
                        'student_name': root.findtext('student_name', ''),
                        'group': root.findtext('group', ''),
                        'subject': root.findtext('subject', ''),
                        'grade': root.findtext('grade', ''),
                        'date': root.findtext('date', ''),
                        'filename': file_path.name
                    }
                    grades.append(data)
            except Exception as e:
                print(f"Ошибка чтения файла {file_path.name}: {e}")
                pass
                
    return grades

def process_uploaded_file(uploaded_file):
    """
    Сохраняет загруженный файл с безопасным именем, проверяет его структуру,
    и удаляет, если он невалиден. Возвращает (Успех(bool), Сообщение(str)).
    """
    ext = Path(uploaded_file.name).suffix.lower()
    
    if ext not in ['.json', '.xml']:
        return False, "Недопустимый формат файла. Разрешены только .json и .xml"

    unique_filename = f"uploaded_{uuid.uuid4().hex}{ext}"
    file_path = STORAGE_DIR / unique_filename

    STORAGE_DIR.mkdir(exist_ok=True)

    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    try:
        if ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            required_keys = {'student_name', 'group', 'subject', 'grade', 'date'}
            if not required_keys.issubset(data.keys()):
                raise ValueError("В JSON отсутствуют обязательные поля успеваемости.")
                
        elif ext == '.xml':
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            required_tags = ['student_name', 'group', 'subject', 'grade', 'date']
            for tag in required_tags:
                if root.find(tag) is None:
                    raise ValueError(f"В XML отсутствует обязательный тег <{tag}>.")
                    
    except Exception as e:
        os.remove(file_path)
        return False, f"Файл не валиден и был удален. Причина: {e}"

    return True, f"Файл успешно загружен и проверен. Сохранен как {unique_filename}"