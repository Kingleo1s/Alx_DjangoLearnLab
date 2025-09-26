from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authors to be viewed or edited.
    Includes nested books via AuthorSerializer.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer



class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    Includes validation for publication_year in BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# ✅ List all books
class BookListView(generics.ListAPIView):
        """
        Provides a GET endpoint to retrieve all books with advanced querying.
        Features:
        - Filter by title, author, publication_year
        - Search by title or author
        - Order by title or publication_year
        Accessible to everyone (read-only).
        """
        queryset = Book.objects.all()
        serializer_class = BookSerializer
        permission_classes = [IsAuthenticatedOrReadOnly]

        # 🔎 Add filters
        filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
        filterset_fields = ['title', 'author', 'publication_year']  # filtering
        search_fields = ['title', 'author__name']  # searching
        ordering_fields = ['title', 'publication_year']  # ordering
        ordering = ['title']  # default ordering


# ✅ Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ✅ Create a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# ✅ Update an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# ✅ Delete a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
