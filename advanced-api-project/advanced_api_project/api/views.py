from api.models import Author, Book
from api.serializers import AuthorSerializer

a1 = Author.objects.create(name="George Orwell")
Book.objects.create(title="1984", publication_year=1949, author=a1)
Book.objects.create(title="Animal Farm", publication_year=1945, author=a1)

serializer = AuthorSerializer(a1)
print(serializer.data)
# Output includes author details + nested books

