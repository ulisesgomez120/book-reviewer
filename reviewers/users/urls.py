from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('create/', views.create, name='create'),
    path('logout/', views.logout, name="logout"),
    path(r'(<user_id>\d+)/', views.show, name="show"),

]
