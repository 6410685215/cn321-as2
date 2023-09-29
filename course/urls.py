from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='course'),
    path('page_user/', views.page_user, name='page_user'),
    path('page_board/', views.page_board, name='page_board'),
    path('page_course/', views.page_course, name='page_course'),
    path('course_enroll/', views.course_enroll, name='course_enroll'),
    path('course_drop/', views.course_drop, name='course_drop'),
]