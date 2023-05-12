from django.urls import path
from .views import Landing, home, BooksView, BooksDetailView, AddReviewView, EditReviewView, ConfirmDeleteReviewView, DeleteReviewView

app_name = "books"
urlpatterns = [
    path("", Landing, name="landing"),
    path("home/", home, name="home"),
    path("books/", BooksView.as_view(), name="list"),
    path("books/<int:id>/", BooksDetailView.as_view(), name="detail"),
    path("books/<int:id>/review/", AddReviewView.as_view(), name="review"),
    path("books/<int:book_id>/review/<int:review_id>/edit/", EditReviewView.as_view(), name="review-edit"),
    path("books/<int:book_id>/review/<int:review_id>/delete/confirm/", ConfirmDeleteReviewView.as_view(), name="confirm-delete-review"),
    path("books/<int:book_id>/review/<int:review_id>/delete/", DeleteReviewView.as_view(), name="delete-review"),

]
# aliklar bolsin