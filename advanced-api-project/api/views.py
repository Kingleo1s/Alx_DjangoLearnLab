from rest_framework import viewsets
from .models import Author
from .serializers import AuthorSerializer
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly

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
    Provides a GET endpoint to retrieve all books.
    Accessible to everyone (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ✅ Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    Provides a GET endpoint to retrieve a book by its ID.
    Accessible to everyone (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ✅ Create a new book
class BookCreateView(generics.CreateAPIView):
    """
    Provides a POST endpoint to add a new book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# ✅ Update an existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    Provides a PUT/PATCH endpoint to modify a book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# ✅ Delete a book
class BookDeleteView(generics.DestroyAPIView):
    """
    Provides a DELETE endpoint to remove a book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]



