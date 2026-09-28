from django.shortcuts import render
from .forms import GradeForm, UploadFileForm
from .utils import save_grade_to_file, get_all_grades, process_uploaded_file

def index(request):
    message = ''
    
    if request.method == 'POST':
        form = GradeForm(request.POST)
        
        if form.is_valid():
            save_grade_to_file(form.cleaned_data)
            message = 'Данные успешно сохранены в файл!'
            form = GradeForm()
    else:
        form = GradeForm()
        
    context = {
        'form': form,
        'message': message
    }
    
    return render(request, 'grades/index.html', context)

def file_list(request):
    grades = get_all_grades()
    
    message = ''
    if not grades:
        message = 'На сервере пока нет ни одного файла с данными (или папка пуста).'
        
    context = {
        'grades': grades,
        'message': message
    }
    
    return render(request, 'grades/file_list.html', context)

def upload_file(request):
    message = ''
    is_error = False
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            file_obj = request.FILES['file']
            success, msg = process_uploaded_file(file_obj)
            
            message = msg
            is_error = not success
            if success:
                form = UploadFileForm()
    else:
        form = UploadFileForm()
        
    context = {
        'form': form,
        'message': message,
        'is_error': is_error
    }
    return render(request, 'grades/upload.html', context)