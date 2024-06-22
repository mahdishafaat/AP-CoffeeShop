from django.shortcuts import render, redirect
from django.views.generic import CreateView
from mainapp.models import Product
def homepage(request):
    return render(request, 'index/index.html', {})

class ProductCreateView(CreateView):
    model=Product
    fields="__all__"