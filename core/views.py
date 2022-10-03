from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PostModelForm, SearchForm
from .models import Post

# Create your views here.

@login_required(login_url="/login/")
def index(request):
    form = PostModelForm(request.POST or None, request.FILES)

    if str(request.method) == "POST":
        if form.is_valid():
            # form.instance.propertier = request.user
            form.save()
            form = PostModelForm()

    posts = Post.objects.all()
    return render(request, "index.html", context={"form": form, "user": request.user, "posts": posts})

@login_required(login_url="/login/")
def search(request):
    form = SearchForm(request.POST or None, request.FILES)

    if str(request.method) == "POST":
        if form.is_valid():
            ...

    return render(request, "search.html", context={"form": form})