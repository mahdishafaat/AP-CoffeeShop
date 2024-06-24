from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView
from mainapp.models import Product
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
def homepage(request):
    return render(request, 'index/index.html', {})


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()

    def handle_no_permission(self):
        return HttpResponse("You do not have permission to view this page")

class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Product
    success_url = reverse_lazy('index')
    fields="__all__"