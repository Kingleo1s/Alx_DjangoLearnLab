
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm, ExampleForm

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
# LibraryProject/bookshelf/views.py




@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


def example_view(request):
    
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process form safely
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            return render(request, "bookshelf/form_example.html", {
                "form": form,
                "success": True,
                "name": name,
            })
    else:
        form = ExampleForm()

    return render(request, "bookshelf/form_example.html", {"form": form})
