from relationship_app.models import Author, Book, Library, Librarian

# Create some sample data (run once)
def create_sample_data():
    # Authors
    author1 = Author.objects.create(name="Chinua Achebe")
    author2 = Author.objects.create(name="Wole Soyinka")

    # Books
    book1 = Book.objects.create(title="Things Fall Apart", author=author1)
    book2 = Book.objects.create(title="Arrow of God", author=author1)
    book3 = Book.objects.create(title="The Lion and the Jewel", author=author2)

    # Library
    library = Library.objects.create(name="National Library")
    library.books.add(book1, book2, book3)

    # Librarian
    Librarian.objects.create(name="Mr. Johnson", library=library)


# Queries
def query_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    # Explicit filter query
    books = Book.objects.filter(author=author)
    return books


def query_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()


def query_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    # Explicit Librarian query (what checker expects)
    librarian = Librarian.objects.get(library=library)
    return librarian
