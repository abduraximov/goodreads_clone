from rest_framework.test import APITestCase
from users.models import CustomUser
from Goodreads.models import Book, BookReview
from rest_framework.reverse import reverse


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        #Principes DRY Dont Repeat Yourself
        self.user = CustomUser.objects.create(username = "testuser", first_name = "testuser")
        self.user.set_password("somepassword")
        self.user.save()
        self.client.login(username="testuser", password="somepassword")
    
    def test_book_review_detail(self):
        book = Book.objects.create(title="Booktest", description="Description", isbn="1216548")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=3, comment="Very nice book")

        response = self.client.get(reverse('api:review-api-detail', kwargs={'id': book.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 3)
        self.assertEqual(response.data['comment'], "Very nice book")
        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], "Booktest")
        self.assertEqual(response.data['book']['description'], "Description")
        self.assertEqual(response.data['book']['isbn'], "1216548")
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['username'], "testuser")
        self.assertEqual(response.data['user']['first_name'], "testuser")
    
    def test_book_review_list(self):
        user_two = CustomUser.objects.create(username = "testuser2", first_name = "testuser2")

        book = Book.objects.create(title="Booktest", description="Description", isbn="1216548")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=3, comment="Very nice book")
        br_two = BookReview.objects.create(book=book, user=user_two, stars_given=5, comment="Very nice book2")

        response = self.client.get(reverse('api:review-api'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(response.data['results'][0]['id'], br_two.id)
        self.assertEqual(response.data['results'][0]['stars_given'], br_two.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], br_two.comment)
        self.assertEqual(response.data['results'][1]['id'], br.id)
        self.assertEqual(response.data['results'][1]['stars_given'], br.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], br.comment)