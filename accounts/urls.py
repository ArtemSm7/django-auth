from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('courses', views.CourseViewSet, basename='api-courses')
router.register('departments', views.DepartmentViewSet, basename='api-departments')
router.register('groups', views.AcademicGroupViewSet, basename='api-groups')

urlpatterns = [
        path(
                'profile/', 
                views.profile, 
                name='profile'
        ),
                
        path(
                'courses/',
                views.course_list, 
                name='course_list'
        ),
        # path(
        #         'courses/add/',
        #         views.course_create,
        #         name='course_create'
        # ),
        # path(
        #         'courses/<int:pk>/edit/',
        #         views.course_update,
        #         name='course_update'
        # ),
        # path(
        #         'courses/<int:pk>/delete/',
        #         views.course_delete,
        #         name='course_delete'
        # ),
        
        path(
                'departments/',
                views.department_list,
                name='department_list'
        ),
        # path(
        #         'departments/add/',
        #         views.department_create,
        #         name='department_create'
        # ),
        # path(
        #         'departments/<int:pk>/edit/',
        #         views.department_update,
        #         name='department_update'
        # ),
        # path(
        #         'departments/<int:pk>/delete/',
        #         views.department_delete,
        #         name='department_delete'
        # ),
        
        path(
                'groups/',
                views.group_list,
                name='group_list'
        ),
        # path(
        #         'groups/add/',
        #         views.group_create,
        #         name='group_create'
        # ),
        # path(
        #         'groups/<int:pk>/edit/',
        #         views.group_update,
        #         name='group_update'
        # ),
        # path(
        #         'groups/<int:pk>/delete/',
        #         views.group_delete,
        #         name='group_delete'
        # ),
        
        path(
                'dashboard/', 
                views.dashboard_view, 
                name='dashboard'
        ),
        
        path('api/', include(router.urls)),
]
