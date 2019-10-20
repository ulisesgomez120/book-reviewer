from django.shortcuts import render, redirect
from .models import User
from books.models import Book
from django.contrib import messages

# Create your views here.


def index(req):
    return render(req, "users/index.html")


def create(req):
    if req.method == 'POST':
        errors = User.objects.validate_register(req.POST)
        if errors:
            for error in errors:
                messages.error(req, error)
            return redirect("users:index")
        user = User.objects.create_user(req.POST)
        req.session['user_id'] = user.id
        return redirect("books:index")
    else:
        return redirect("users:index")


def login(req):
    if req.method == 'POST':
        valid, response = User.objects.validate_login(req.POST)
        if not valid:
            messages.error(req, response)
            return redirect("users:index")
        req.session['user_id'] = response.id
        return redirect("books:index")


def logout(req):
    req.session.clear()
    messages.error(req, "You have been successfully logged out")
    return redirect("users:index")


def show(req, user_id):
    if "user_id" not in req.session:
        return redirect("users:index")
    user_data = User.objects.get(id=user_id).__dict__
    clean_user = {
        'first_name': user_data['first_name'],
        'last_name': user_data['last_name'],
        'email': user_data['email'],
        'id': user_data['id']
    }
    context = {
        "user": clean_user,
        'books': User.objects.get(id=user_id).reviews.all(),
        "count": User.objects.get(id=user_id).reviews.count(),
    }

    return render(req, "users/show.html", context)
