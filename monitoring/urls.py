from django.urls import path

from . import views


urlpatterns = [
    path('update_data/', views.update_data),
]
