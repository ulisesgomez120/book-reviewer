from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.new, name="new"),
    path('create_book/', views.create_book, name="create_book"),
    path(r'add_review/(<book_id>\d+)/', views.add_review, name="add_review"),
    path(r'(<book_id>\d+)/', views.show, name="show"),

]
