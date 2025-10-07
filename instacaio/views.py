from django.shortcuts import render, redirect
from django.http import HttpRequest
from instacaio.forms import PostForm
from instacaio.models import Post
from django.contrib.auth.decorators import login_required

def inicio(request):
    posts = Post.objects.filter(aprovado = True)
    return render(request, 'inicio.html', {
        'posts': posts
    })

@login_required(login_url="/contas/login/")
def criar_post(request: HttpRequest):
    if (request.method == "POST"):
        formulario = PostForm(request.POST, request.FILES)
        if (formulario.is_valid):
            post:Post = formulario.save(commit = False)
            post.autor = request.user
            if request.user.is_staff:
                post.aprovado = True
            post.save()
            return redirect("inicio")
    else:
        formulario = PostForm()
    return render(request, 'postar.html', {
        "formulario": formulario
    })

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registrar.html', {'form': form})