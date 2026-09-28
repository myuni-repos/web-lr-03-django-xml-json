from django.shortcuts import render
from .forms import GradeForm
from .utils import save_grade_to_file, get_all_grades

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