from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.views import View
from .forms import *

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse


from .models import Book
from django.shortcuts import render, redirect, get_object_or_404
from dz import settings


from django.core.files import File
from django.core.files.storage import FileSystemStorage

from django.conf.urls import url
from django.contrib.staticfiles.templatetags.staticfiles import static
import os


class BaseView(View):
    def render(self, request, template, context):
        context.update({
            'authorized': request.user.is_authenticated,
            'user': {'name': request.user.username},
        })

        return render(request, template, context)


class LogView(BaseView):
    def get(self, request):
        if request.user.is_authenticated:
            auth.logout(request)

        return BaseView.render(self, request, 'login.html', {
                'login_form': AuthForm(),
            })

    def post(self, request):
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        return BaseView.render(self, request, 'login.html', {
                'login_form': AuthForm(),
                'error': 'Wrong username/password'
            })


class RegView(BaseView):
    def get(self, request):
        if request.user.is_authenticated:
            auth.logout(request)

        return BaseView.render(self, request, 'registr.html', {
                'registration_form': RegistrationForm(),
        })

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect('/')

        return BaseView.render(self, request, 'registr.html', {
                'registration_form': RegistrationForm(),
                'error': form.errors.popitem()[1]
        })


class BooksList(BaseView):
    def get(self, request):
        books = Book.objects.all()
        return super().render(request, 'list.html', {'alert': settings.MEDIA_ROOT,
                                                     'books': books,
                                                     'new_book_form': AddBookForm()})


def add_new_book(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    form = AddBookForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            book = form.fill_object()
            book.save()
            return redirect('single_book', book_id=book.id)


class ObjectView(BaseView):
    def get(self, request, book_id):
        obj = get_object_or_404(Book, id=book_id)
        id = request.user.id

        return super().render(
            request,
            'book.html',
            context={
                'book': obj,
                'status': obj.participation.filter(id=id).exists(),
                'users': obj.participation.all()
            }
        )

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)

        if request.user.is_authenticated():
            state = request.POST.get('state')
            if state == 'True' and not book.participation.filter(id=request.user.id).exists():
                book.participation.add(request.user)

            if state == 'False' and book.participation.filter(id=request.user.id).exists():
                book.participation.remove(request.user)

            listusers = list(book.participation.all())

            return HttpResponse(', '.join(str(e) for e in listusers))
        return HttpResponse('error')
