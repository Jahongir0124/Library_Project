from re import template
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView,DetailView
from .models import *

# Create your views here.


class Index(ListView):
    model = Books
    paginate_by = 3
    context_object_name = 'book_list'
    template_name = 'home.html'
    category = Category.objects.all()
    extra_context = {'title':'Bosh sahifa','cat':category}


class Categorybook(ListView):
    model = Books
    context_object_name = 'book_list'
    paginate_by = 3
    template_name = 'home.html'
    cat = Category.objects.all()
    extra_context = {'cat': cat}
    def get_queryset(self):
        category = Category.objects.filter(slug=self.kwargs['slug'])
        book = Books.objects.filter(cname=self.kwargs['slug'])
        return book
class DisCounts(ListView):
    model = Books
    context_object_name = 'book_list'
    template_name = 'discount.html'
    def get_queryset(self):
        return HttpResponse('Hozirda Chegirmalar mavjud emas')
class InfoBook(ListView):
    model = Books
    context_object_name = 'book_info'
    template_name = 'book_info.html'
    extra_context = {}
    def get_queryset(self):
        data = Books.objects.filter(slug=self.kwargs['slug'])
        comment = Comments.objects.filter(book=data[0].id)
        self.extra_context['comment'] = comment
        return data

    def post(self,request, *args, **kwargs):
        book = Books.objects.get(slug=self.kwargs['slug'])
        txt = request.POST.get('t')
        user = request.user.first_name+' '+request.user.last_name
        email = request.user.email
        com = Comments(book=book,text=txt,username=user,email=email)
        com.save()
        return redirect("unique_slug",slug=self.kwargs['slug'])   

class Search(ListView):
    model = Books
    context_object_name = 'book_list'
    template_name = 'home.html'
    try:
        @method_decorator(csrf_exempt)
        def get_queryset(self):
            if 'q' in self.request.GET:
                data = self.request.GET['q']
                if len(data) > 0:
                    if data.isdigit():
                        book = Books.objects.filter(price=data)
                        return book
                    else:
                        book = Books.objects.filter(Q(name__contains=data) | Q(description__contains=data))
                        print(book)
                        return book
                else:
                    return HttpResponse('Qidiruv kalit so\'zini kiriting')
    except Exception as e:
        pass
    
class NewBooks(ListView):
    model = Books
    template_name = 'home.html'
    context_object_name = 'book_list'
    paginate_by = 3
    def get_queryset(self):
        book = Books.objects.all().order_by('-created_time')[:5]
        return book



        

