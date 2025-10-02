from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import Post
from django.forms.widgets import Textarea
from .models import Comment

# Registration form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Update user basic info
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


# Update user profile (extra fields)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile    # assumes you created a Profile model in models.py
        fields = ['bio', 'image']   # or whatever fields you added


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "content": Textarea(attrs={"rows": 10, "placeholder": "Write your post here..."}),
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Leave a respectful comment..."
            })
        }

    def clean_content(self):
        content = (self.cleaned_data.get("content") or "").strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        if len(content) < 2:
            raise forms.ValidationError("Comment is too short.")
        return content
