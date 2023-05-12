from django.test import TestCase
from django.urls import reverse
from .models import Book, CustomUser, BookReview, Author, BookAuthor

class BooksTestCase(TestCase):
    def test_no_books(self):
        respone = self.client.get(reverse("books:list"))

        self.assertContains(respone, "No books found.")

    def test_books_list(self):
        book1 = Book.objects.create(title="Booktest", description="Description", isbn="1216548")
        book2 = Book.objects.create(title="Booktest1", description="Description1", isbn="12165481")
        book3 = Book.objects.create(title="Booktest2", description="Description2", isbn="12165482")

        response = self.client.get(reverse("books:list") + "?page_size=2")
        # book = Book.objects.all()
        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)
        
        response = self.client.get(reverse("books:list") + "?page=2&page_size=2")
        self.assertContains(response, book3.title)

    def test_detail_page(self):

        book = Book.objects.create(title="Booktest", description="Description", isbn="1216548")
        author = Author.objects.create(first_name="Joy", last_name="Kind")
        book_author = BookAuthor.objects.create(book=book, author=author)

        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
        self.assertContains(response, book.isbn)
        self.assertContains(response, book_author.author.full_name())

        self.assertEqual(response.status_code, 200)
    

    def test_search_books(self):

        book1 = Book.objects.create(title="Salom", description="Description", isbn="1216548")
        book2 = Book.objects.create(title="Dunyo", description="Description1", isbn="12165481")
        book3 = Book.objects.create(title="Hushkelibsiz", description="Description2", isbn="12165482")

        response = self.client.get(reverse("books:list") + "?q=salom")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=nyo")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=kelibsiz")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)

class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title="Booktest", description="Description", isbn="1216548")

        user = CustomUser.objects.create(
            username = "user1", first_name = "user1", last_name = "user1", email = "user1@bk.ru" 
        )
        user.set_password("somepass")
        user.save()

        self.client.login(username="user1", password="somepass")

        response = self.client.post(reverse("books:review", kwargs={"id": book.id}), data={
            "stars_given": 3,
            "comment": "nice book"
        })

        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "nice book")
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)

class HomePageTestCase(TestCase):
    def test_pagineted_list(self):
        book = Book.objects.create(title="Booktest", description="Description", isbn="1216548")

        user = CustomUser.objects.create(
            username = "user1", first_name = "user1", last_name = "user1", email = "user1@bk.ru" 
        )
        user.set_password("somepass")
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=3, comment="nice book")
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment="very nice book")
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment="amazing book")

        response = self.client.get(reverse("books:home") + "?page_size=3")

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertContains(response, review1.comment)
