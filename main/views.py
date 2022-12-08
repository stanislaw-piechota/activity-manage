from django.shortcuts import render, redirect
from .models import *

def main(request):
    if request.method == 'POST':
        if request.POST.get('manage'):
            return redirect('./manage')
    return render(request, 'main/index.html', {})

def manage(request):
    if 'teacher' not in request.session.keys():
        request.session['teacher'] = False
    payload = {
        'verified': request.session['teacher'], 
        'classes':[],
        'select': request.COOKIES.get('class'),
        'students': [],
        'visible': []
    }

    if payload['verified']:
        classes = list(set([obj.class_name for obj in Student.objects.all()]))
        payload['classes'] = classes
        
        if payload.get('select') and payload.get('select') != 'Wybierz':
            students = Student.objects.filter(class_name=payload.get('select'))
            payload['students'] = students
            visible = students.filter(visibility=True).order_by('grades','pluses')
            payload['visible'] = visible
    
    if request.method == "POST":
        if request.POST.get('pin'):
            codes = Code.objects.filter(code=request.POST.get('pin'))
            if len(codes):
                code = codes[0]
                if code.admin:
                    request.session['teacher'] = True
                    return redirect('/manage')
        if request.POST.get('refresh'):
            for student in Student.objects.filter(class_name=payload['select']):
                if request.POST.get(f'check-{student.number}'):
                    student.visibility = True
                else:
                    student.visibility = False
                student.save()
            return redirect('/manage')
        if request.POST.get("adding"):
            num = int(request.POST.get("adding").split('-')[1])
            student = Student.objects.get(number=num, class_name=payload['select'])
            student.pluses += 1
            if student.pluses >= 6:
                student.pluses = 0
                student.grades += 1
            student.visibility = False
            student.save()
            return redirect('/manage')

        

    return render(request, 'main/manage.html', payload)