
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book
<<<<<<< HEAD
from .forms import BookForm
=======
from .forms import ExampleForm
>>>>>>> 2060982dd9b3b3ece3275acf91fb247f5f8822b2

# Protect with permission check and raise_exception=True
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

<<<<<<< HEAD
# LibraryProject/bookshelf/views.p

@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/form_example.html', {'form': form, 'book': book})

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('bookshelf:book_list')
    return render(request, 'bookshelf/delete_book.html', {'book': book})


=======

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
>>>>>>> 2060982dd9b3b3ece3275acf91fb247f5f8822b2
