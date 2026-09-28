from django import forms
import datetime

class GradeForm(forms.Form):
    FORMAT_CHOICES = [
        ('json', 'JSON'),
        ('xml', 'XML')
    ]

    student_name = forms.CharField(max_length=100, label="Имя студента")
    group = forms.CharField(max_length=20, label="Группа")
    subject = forms.CharField(max_length=100, label="Предмет")    
    grade = forms.IntegerField(min_value=1, max_value=5, label="Оценка")
    date = forms.DateField(
        initial=datetime.date.today,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата сдачи"
    )
    file_format = forms.ChoiceField(choices=FORMAT_CHOICES, label="Формат сохранения")


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Выберите XML или JSON файл")