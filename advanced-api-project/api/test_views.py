from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITests(APITestCase):
    """
    Unit tests for the Book API endpoints.
    Covers CRUD, permissions, filtering, searching, and ordering.
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        # Create an author
        self.author = Author.objects.create(name="Test Author")

        # Create some books
        self.book1 = Book.objects.create(title="Alpha Book", publication_year=2000, author=self.author)
        self.book2 = Book.objects.create(title="Beta Book", publication_year=2010, author=self.author)

        # Common endpoints
        self.book_list_url = reverse("book-list")       # /books/
        self.book_detail_url = reverse("book-detail", args=[self.book1.id])  # /books/<id>/

    # --- LIST & DETAIL ---

    def test_list_books(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)  # At least 2 books

    def test_retrieve_book(self):
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    # --- CREATE (requires auth) ---

    def test_create_book_unauthenticated(self):
        data = {"title": "Unauthorized Book", "publication_year": 2025, "author": self.author.id}
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        self.client.login(username="testuser", password="testpass123")
        data = {"title": "New Book", "publication_year": 2022, "author": self.author.id}
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # --- UPDATE (requires auth) ---

    def test_update_book_authenticated(self):
        self.client.login(username="testuser", password="testpass123")
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.put(url, {"title": "Updated Book", "publication_year": 2001, "author": self.author.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book")

    # --- DELETE (requires auth) ---

    def test_delete_book_authenticated(self):
        self.client.login(username="testuser", password="testpass123")
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    # --- FILTERING / SEARCH / ORDERING ---

    def test_filter_books_by_year(self):
        response = self.client.get(self.book_list_url, {"publication_year": 2010})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Beta Book")

    def test_search_books_by_title(self):
        response = self.client.get(self.book_list_url, {"search": "Alpha"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Alpha Book")

    def test_order_books_by_title(self):
        response = self.client.get(self.book_list_url, {"ordering": "title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, sorted(titles))
