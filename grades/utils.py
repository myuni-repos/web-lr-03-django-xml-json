import json
import xml.etree.ElementTree as ET
import uuid
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