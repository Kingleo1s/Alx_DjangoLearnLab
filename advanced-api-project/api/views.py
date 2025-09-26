from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


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
