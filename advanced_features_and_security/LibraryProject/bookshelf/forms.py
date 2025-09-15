from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]

class ExampleForm(forms.Form):
    """A simple example form to demonstrate CSRF protection and validation."""
    name = forms.CharField(max_length=100, required=True, label="Your Name")
    email = forms.EmailField(required=True, label="Your Email")
    message = forms.CharField(
        widget=forms.Textarea,
        required=True,
        label="Message"
    )

