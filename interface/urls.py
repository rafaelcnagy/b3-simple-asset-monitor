from django.urls import path

from . import views


urlpatterns = [
    path('', views.view_list, name='view_list'),
    path('update/<id>', views.update, name='update'),
    path('register/', views.register, name='register'),
    path('delete/<id>', views.delete, name='delete'),

]
