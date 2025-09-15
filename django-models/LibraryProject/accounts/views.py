from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test


# --- Helper check functions ---
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"


def is_librarian(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"


def is_member(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Member"


# --- Views ---
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "accounts/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "accounts/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    return render(request, "accounts/member_view.html")
