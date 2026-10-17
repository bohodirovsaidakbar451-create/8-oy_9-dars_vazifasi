from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Genre, Book
from .serializers import BookDetailSerializer


class BookTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="Toxir")
        self.admin = User.objects.create(username="Admin", is_staff=True, is_superuser=True)

        self.genre1 = Genre.objects.create(name="Roman")
        self.genre2 = Genre.objects.create(name="Detektiv")

        self.book1 = Book.objects.create(title="O'tkan kunlar", author="Abdulla Qodiriy", price=50000, published_year=1926, genre=self.genre1)
        self.book2 = Book.objects.create(title="Mehrobdan chayon", author="Abdulla Qodiriy", price=45000, published_year=1929, genre=self.genre1)
        self.book3 = Book.objects.create(title="Sherlok Holms", author="Artur Konan Doyl", price=60000, published_year=1892, genre=self.genre2)

    def test_get(self):
        url = reverse('book-list')

        self.client.force_login(self.user1)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        serializer = BookDetailSerializer([self.book3, self.book2, self.book1], many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_search(self):
        url = reverse('book-list')

        self.client.force_login(self.user1)
        response = self.client.get(url, data={'search': 'kun'})

        self.assertEqual(response.status_code, 200)
        serializer = BookDetailSerializer([self.book1], many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_filter(self):
        url = reverse('book-list')

        self.client.force_login(self.user1)
        response = self.client.get(url, data={'genre': self.genre1.id})

        self.assertEqual(response.status_code, 200)
        serializer = BookDetailSerializer([self.book2, self.book1], many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_pagination(self):
        url = reverse('book-list')

        self.client.force_login(self.user1)
        response = self.client.get(url, data={'limit': 2, 'offset': 1})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 3)
        serializer = BookDetailSerializer([self.book2, self.book1], many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_detail(self):
        url = reverse('book-detail', args=[self.book1.id])

        self.client.force_login(self.user1)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        serializer = BookDetailSerializer(self.book1)
        self.assertEqual(response.data, serializer.data)

    def test_post_admin(self):
        url = reverse('book-list')
        data = {
            'title': "Sariq devni minib",
            'author': "Xudoyberdi To'xtaboyev",
            'price': 40000,
            'published_year': 1976,
            'genre': self.genre1.id
        }

        self.client.force_login(self.admin)
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 4)

    def test_post_user(self):
        url = reverse('book-list')
        data = {
            'title': "Sariq devni minib",
            'author': "Xudoyberdi To'xtaboyev",
            'price': 40000,
            'published_year': 1976,
            'genre': self.genre1.id
        }

        self.client.force_login(self.user1)
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Book.objects.count(), 3)

    def test_put_admin(self):
        url = reverse('book-detail', args=[self.book1.id])
        data = {
            'title': "O'tkan kunlar",
            'author': "Abdulla Qodiriy",
            'price': 70000,
            'published_year': 1926,
            'genre': self.genre1.id
        }

        self.client.force_login(self.admin)
        response = self.client.put(url, data=data)

        self.assertEqual(response.status_code, 200)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.price, 70000)

    def test_delete_admin(self):
        url = reverse('book-detail', args=[self.book1.id])

        self.client.force_login(self.admin)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Book.objects.count(), 2)

    def test_delete_user(self):
        url = reverse('book-detail', args=[self.book1.id])

        self.client.force_login(self.user1)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Book.objects.count(), 3)
