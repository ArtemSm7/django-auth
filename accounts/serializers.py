from rest_framework import serializers
from .models import Course, Department, AcademicGroup

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')
        
class AcademicGroupSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = AcademicGroup
        fields = ('id', 'name', 'department', 'department_name')
        
class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source='department.name',
        read_only=True
    )
    
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'department', 'department_name')
        
    def validate_title(self, value):
        """Базовая валидация: очистка от лишних пробелов и проверка длины."""
        clean_title = value.strip()
        if len(clean_title) < 5:
            raise serializers.ValidationError(
                "Название курса должно содержать не менее 5 символов."
            )
        return clean_title
    
    def validate(self, attrs):
        """Бизнес-правило: защита целостности учебного процесса."""
        if self.instance is not None:
            old_department = self.instance.department
            new_department = attrs.get('department', old_department)
            if old_department != new_department:
                if self.instance.students.exists():
                    raise serializers.ValidationError({
                        "department": "Невозможно изменить факультет курса, если у него есть студенты."
                    })
        return attrs