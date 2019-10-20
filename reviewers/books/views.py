from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from users.models import User
from .models import Book, Author, Review

# Create your views here.


def index(req):
    if "user_id" not in req.session:
        messages.error(req, "You are not logged in")
        return redirect("users:index")
    user_data = User.objects.get(id=req.session['user_id']).__dict__
    clean_user = {
        'first_name': user_data['first_name'],
        'last_name': user_data['last_name'],
        'email': user_data['email'],
        'id': user_data['id']
    }
    average_rating = []
    for obj in Review.objects.order_by("-created_at")[:3]:
        rating_sum = 0
        book = obj.book
        for review in book.reviews.all():
            rating_sum += review.rating
        average = rating_sum / book.reviews.all().count()
        average_rating.append(average)
    context = {
        "user": clean_user,
        "books": Book.objects.order_by('name'),
        "recent": Review.objects.order_by("-created_at")[:3],
        'average_rating': average_rating,
    }
    return render(req, "books/index.html", context)


def new(req):
    context = {
        'authors': Author.objects.all(),
    }
    return render(req, "books/new_book.html", context)


def create_book(req):
    if req.method == "POST":
        errors = Book.objects.validate_book(req.POST)
        if errors:
            for error in errors:
                messages.error(req, error)
            return redirect("books:new")
        book_id = Book.objects.create_book(req.POST, req.session['user_id'])
    return redirect("books:show", book_id=book_id)


def show(req, book_id):
    rating_sum = 0
    for review in Book.objects.get(id=book_id).reviews.all():
        rating_sum += review.rating
    average = rating_sum / Book.objects.get(id=book_id).reviews.all().count()

    context = {
        "book": Book.objects.get(id=book_id),
        "reviews": Book.objects.get(id=book_id).reviews.all(),
        "average_rating": average,
    }
    return render(req, "books/show.html", context)


def add_review(req, book_id):
    if req.method == "POST":
        error = Book.objects.validate_review(req.POST)
        if error != '':
            messages.error(req, error)
            return redirect("books:show", book_id)
        Book.objects.add_review(req.POST, book_id, req.session['user_id'])
        return redirect("books:show", book_id)
