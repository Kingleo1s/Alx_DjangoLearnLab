
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book

# Protect with permission check and raise_exception=True
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # Query all books
    books = Book.objects.all()
    # Pass them into the template context
    return render(request, 'bookshelf/book_list.html', {'books': books})


def search_books(request):
    query = request.GET.get("q", "")
    books = Book.objects.filter(title__icontains=query)  # ORM prevents SQL injection
    return render(request, "bookshelf/book_list.html", {"books": books})
