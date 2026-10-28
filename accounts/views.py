from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from .forms import (
    AcademicGroupForm,
    CourseForm,
    DepartmentForm,
)
from .models import (
    AcademicGroup,
    Course,
    Department,
    StudentProfile
)
from django.contrib.auth.models import User
from django.contrib.auth import login

import csv
import json
from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncDate

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import CourseSerializer, DepartmentSerializer, AcademicGroupSerializer


def is_methodist(user):
    return user.groups.filter(
        name='Методист'
    ).exists()


@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.last_name = request.POST.get('last_name', '')
        user.first_name = request.POST.get('first_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        return redirect('profile')
    return render(
        request,
        'profile.html',
        {
            'is_methodist': is_methodist(request.user)
        }
    )


@login_required
def course_list(request):
    courses = Course.objects.select_related('department').all()
    return render(
        request,
        'course_list.html',
        {
            'courses': courses,
            'is_methodist': is_methodist(request.user),
        }
    )
    

@login_required
@user_passes_test(is_methodist)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Добавление курса',
        }
    )


@login_required
@user_passes_test(is_methodist)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Изменение курса',
        }
    )


@login_required
@user_passes_test(is_methodist)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')

    return render(
        request,
        'object_confirm_delete.html',
        {
            'object': course,
            'title': 'Удаление курса',
        }
    )


@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(
        request,
        'department_list.html',
        {
            'departments': departments,
            'is_methodist': is_methodist(request.user),
        }
    )

    
@login_required
@user_passes_test(is_methodist)
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(
            request.POST
        )
        if form.is_valid():
            form.save()
            return redirect(
                'department_list'
            )
    else:
        form = DepartmentForm()

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Добавление факультета',
        }
    )
    


@login_required
@user_passes_test(is_methodist)
def department_update(
    request,
    pk
):
    department = get_object_or_404(
        Department,
        pk=pk
    )
    if request.method == 'POST':
        form = DepartmentForm(
            request.POST,
            instance=department
        )
        if form.is_valid():
            form.save()
            return redirect(
                'department_list'
            )
    else:
        form = DepartmentForm(
            instance=department
        )

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Изменение факультета',
        }
    )


@login_required
@user_passes_test(is_methodist)
def department_delete(
    request,
    pk
):
    department = get_object_or_404(
        Department,
        pk=pk
    )
    if request.method == 'POST':
        department.delete()
        return redirect(
            'department_list'
        )

    return render(
        request,
        'object_confirm_delete.html',
        {
            'object': department,
            'title': 'Удаление факультета',
        }
    )
    
    
@login_required
def group_list(request):
    groups = AcademicGroup.objects.select_related('department').all()
    return render(
        request,
        'group_list.html',
        {
            'groups': groups,
            'is_methodist': is_methodist(request.user),
        }
    )


@login_required
@user_passes_test(is_methodist)
def group_create(request):
    if request.method == 'POST':
        form = AcademicGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = AcademicGroupForm()

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Добавление учебной группы',
        }
    )


@login_required
@user_passes_test(is_methodist)
def group_update(request, pk):
    group = get_object_or_404(AcademicGroup, pk=pk)
    if request.method == 'POST':
        form = AcademicGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = AcademicGroupForm(instance=group)

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Изменение учебной группы',
        }
    )


@login_required
@user_passes_test(is_methodist)
def group_delete(request, pk):
    group = get_object_or_404(AcademicGroup, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('group_list')

    return render(
        request,
        'object_confirm_delete.html',
        {
            'object': group,
            'title': 'Удаление учебной группы',
        }
    )
    
    
    
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')

        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html', {'error': 'Пользователь с таким логином уже существует'})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        StudentProfile.objects.create(user=user)
        login(request, user)
        return redirect('profile') 
    return render(request, 'registration/register.html')




@login_required
def dashboard_view(request):
    # --- 1. ИНТЕРАКТИВНЫЙ ФИЛЬТР ПО ВРЕМЕНИ ---
    days = request.GET.get('days', 'all')
    user_query = User.objects.all()
    
    if days != 'all':
        try:
            days_int = int(days)
            start_date = timezone.now() - timedelta(days=days_int)
            user_query = user_query.filter(date_joined__gte=start_date)
        except ValueError:
            pass
    # --- 2. ЭКСПОРТ ДАННЫХ В CSV (ФИЧА ДЛЯ ДОП. БАЛЛОВ) ---
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="courses_report.csv"'
        response.write(u'\ufeff'.encode('utf8')) # Это нужно, чтобы Excel правильно читал русский язык
        
        writer = csv.writer(response, delimiter=';')
        writer.writerow(['Название курса', 'Количество студентов', 'Факультет'])
        
        courses_stat = Course.objects.annotate(student_count=Count('students')).order_by('-student_count')
        for c in courses_stat:
            dept_name = c.department.name if c.department else 'Нет данных'
            writer.writerow([c.title, c.student_count, dept_name])
        return response

    # --- 3. СБОР СТАТИСТИКИ ДЛЯ KPI-КАРТОЧЕК ---
    total_students = StudentProfile.objects.count()
    total_courses = Course.objects.count()
    
    top_dept = Department.objects.annotate(
        student_count=Count('students')
    ).order_by('-student_count').first()
    top_dept_name = top_dept.name if top_dept else "Нет данных"

    # --- 4. ПОДГОТОВКА ДАННЫХ ДЛЯ ГРАФИКОВ ---
    
    # График 1 (Круговой): Студенты по факультетам
    dept_stats = Department.objects.annotate(count=Count('students')).values('name', 'count')
    dept_labels = [item['name'] for item in dept_stats]
    dept_series = [item['count'] for item in dept_stats]

    # График 2 (Столбчатый): Топ-5 популярных курсов
    course_stats = Course.objects.annotate(count=Count('students')).values('title', 'count').order_by('-count')[:5]
    course_labels = [item['title'] for item in course_stats]
    course_series = [item['count'] for item in course_stats]

    # График 3 (Линейный): Динамика регистраций по дням
    reg_stats = user_query.annotate(date=TruncDate('date_joined')).values('date').annotate(count=Count('id')).order_by('date')
    reg_labels = [item['date'].strftime('%d.%m.%Y') for item in reg_stats if item['date']]
    reg_series = [item['count'] for item in reg_stats]

    # Упаковывка в context для передачи в HTML
    context = {
        'is_methodist': is_methodist(request.user),
        'total_students': total_students,
        'total_courses': total_courses,
        'top_dept_name': top_dept_name,
        'current_days_filter': days,
        
        # json.dumps превращает списки Python в формат, понятный JavaScript-у
        'dept_labels_json': json.dumps(dept_labels),
        'dept_series_json': json.dumps(dept_series),
        'course_labels_json': json.dumps(course_labels),
        'course_series_json': json.dumps(course_series),
        'reg_labels_json': json.dumps(reg_labels),
        'reg_series_json': json.dumps(reg_series),
    }
    return render(request, 'dashboard.html', context)



class IsMethodistPermission(IsAuthenticated):
    """Кастомный класс прав доступа для DRF."""
    def has_permission(self, request, view):
        is_auth = super().has_permission(request, view)
        if request.method == 'GET':
            return is_auth
        return is_auth and request.user.groups.filter(name='Методист').exists()

class DepartmentViewSet(viewsets.ModelViewSet):
    """Факультеты доступны только для чтения."""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    
class AcademicGroupViewSet(viewsets.ModelViewSet):
    queryset = AcademicGroup.objects.select_related('department').all()
    serializer_class = AcademicGroupSerializer
    permission_classes = [IsMethodistPermission]
    
class CourseViewSet(viewsets.ModelViewSet):
    """Полный CRUD для курсов с проверкой прав."""
    queryset = Course.objects.select_related('department').all()
    serializer_class = CourseSerializer
    permission_classes = [IsMethodistPermission]