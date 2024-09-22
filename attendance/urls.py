from django.urls import path
from . import views

urlpatterns = [
    path('', views.sub_index, name='sub_index'),
    path('validate_user/', views.validate_user, name='validate_user'),
    path('capture_image/', views.capture_image_view, name='capture_image'),
    path('mark/', views.mark, name='mark'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('add/',views.add,name="add"),
    path('index/', views.index, name='index'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact')
]
