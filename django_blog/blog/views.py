
from django.contrib.auth import login
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from .forms import PostForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from .models import Post,Comment
from .forms import CommentForm
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views.generic import UpdateView, DeleteView
from .models import Tag



def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # optionally log user in immediately
            messages.success(request, "Registration successful. Welcome!")
            return redirect("blog:profile")
    else:
        form = SignUpForm()
    return render(request, "blog/register.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("blog:profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "blog/profile.html", context)
@login_required

def home(request):
    return render(request, "blog/home.html")

def post_list(request):
    return render(request, 'blog/post_list.html')

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"   # blog/templates/blog/post_list.html
    context_object_name = "posts"
    paginate_by = 10
    ordering = ["-published_date"]

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = CommentForm()
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # handle tags (list from cleaned_data)
        tag_names = form.cleaned_data.get("tags", []) or []
        self.object.tags.clear()
        for name in tag_names:
            tag_obj, _ = Tag.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
            self.object.tags.add(tag_obj)
        return response

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_initial(self):
        initial = super().get_initial()
        # prefill tags field as comma-separated names
        initial_tags = ", ".join([t.name for t in self.get_object().tags.all()])
        initial["tags"] = initial_tags
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        tag_names = form.cleaned_data.get("tags", []) or []
        self.object.tags.clear()
        for name in tag_names:
            tag_obj, _ = Tag.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
            self.object.tags.add(tag_obj)
        return response

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Tag view: show posts for a tag
def tag_posts(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = tag.posts.order_by("-published_date").all()
    context = {"tag": tag, "posts": posts}
    return render(request, "blog/tag_posts.html", context)

# Search view
def search(request):
    q = request.GET.get("q", "").strip()
    results = []
    if q:
        # search title, content, and tags (tag name)
        results = Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct().order_by("-published_date")
    context = {"query": q, "results": results}
    return render(request, "blog/search_results.html", context)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.kwargs['post_pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
