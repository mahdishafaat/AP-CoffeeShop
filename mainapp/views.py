from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView
from mainapp.models import Product
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
def homepage(request):
    return render(request, 'index/index.html', {})

def store_view(request):
    all_products = Product.objects.all()
    context={'products':all_products}
    return render(request,'mainapp/store.html',context=context)



class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()

    def handle_no_permission(self):
        return HttpResponse("You do not have permission to view this page")

class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Product
    fields = ['category',
        'name', 'description', 'price', 'timeNeeded', 'coffee', 'milk', 
        'chocolate', 'flour', 'sugar', 'image'
    ]
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        print("Form is valid")
        return super().form_valid(form)


    def form_invalid(self, form):
        print("Form is invalid")
        print(form.errors.as_data())  # Print the errors to console
        return super().form_invalid(form)