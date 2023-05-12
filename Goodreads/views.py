from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from .models import Book, BookReview
from .forms import BookReviewForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

def Landing(request):
    return render(request, 'landing.html')

def home(request):
    reviews = BookReview.objects.all().order_by("-created_at")
    page_size = request.GET.get('page_size', 10)
    paginator = Paginator(reviews, page_size)

    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    return render(request, "home.html", {"page_obj": page_obj})



# with generics ListViews
# class BooksView(ListView):
#     template_name = "books/list.html"
#     queryset = Book.objects.all()
#     context_object_name = "books"
#     paginate_by = 2

class BooksView(View):
    def get(self, request):
        books = Book.objects.all().order_by("id")
        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains = search_query)
        page_size = request.GET.get('page_size', 4)
        pagination = Paginator(books, page_size)

        page_num = request.GET.get('page', 1)
        page_obj = pagination.get_page(page_num)

        return render(request, "books/list.html", { "books": page_obj, "search_query": search_query } )

# with generics DetailViews

# class BooksDetailView(DetailView):
#     template_name = "books/detail.html"
#     pk_url_kwarg = "id"
#     model = Book
#     context_object_name = "detail"


class BooksDetailView(View):
    def get(self, request, id):
        detail = Book.objects.get(id=id)
        review_form = BookReviewForm
        return render(request, "books/detail.html", { "detail": detail, "review_form": review_form})

class AddReviewView(View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment']
            )

            return redirect(reverse("books:detail", kwargs={"id": book.id}))
        
        return render(request, "books/detail.html", { "detail": book, "review_form": review_form})
class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)
        review_form = BookReviewForm(instance=review)
        
        return render(request, "books/edit_review.html", { "review": review, "book": book, "review_form": review_form})
    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse("books:detail", kwargs={"id": book.id}))
        return render(request, "books/edit_review.html", { "review": review, "book": book, "review_form": review_form})

class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)

        return render(request, "books/confirm_delete_review.html", { "book": book, "review": review })

class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)

        review.delete()
        messages.success(request, "You have successfully deleted this review")

        return redirect(reverse("books:detail", kwargs={"id": book.id}))