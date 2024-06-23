from django.shortcuts import render, redirect
from django.views.generic import CreateView
from mainapp.models import Product
from django.urls import reverse_lazy
def homepage(request):
    return render(request, 'index/index.html', {})

class ProductCreateView(CreateView):
    model = Product
    success_url = reverse_lazy('index')
    fields="__all__"