from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView,UpdateView
from mainapp.models import Product, Order,Storage
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count

def homepage(request):
    top_selling_products = Product.objects.order_by('-sold_count')[:12]
    context = {
        'products': top_selling_products
    }
    return render(request, 'index/index.html',context=context)

def store_view(request):
    all_products = Product.objects.all()
    context={'products':all_products}
    return render(request,'mainapp/store.html',context=context)



class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()

    def handle_no_permission(self):
        return HttpResponse("You do not have permission to view this page <br><a href='http://127.0.0.1:8000/accounts/login'>login</a>")

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
        print(form.errors.as_data())
        return super().form_invalid(form)

def select_storage_view(request):
    storages = Storage.objects.all()
    return render(request, 'mainapp/select_storage.html', {'storages': storages})


class StorageUpdateView(UpdateView):
    model=Storage
    fields="__all__"
    success_url = reverse_lazy('index')

def is_staff(user):
    return user.is_staff

# @user_passes_test(is_staff)
def management_panel(request):
    product_sales = (
        Order.objects.values('products__name', 'products__category')
        .annotate(count=Count('products'))
        .order_by('products__category', 'products__name')
    )
    
    chart_data = {}
    for sale in product_sales:
        category = sale['products__category']
        product = sale['products__name']
        count = sale['count']
        if category not in chart_data:
            chart_data[category] = []
        chart_data[category].append({'product': product, 'count': count})

    context = {
        'chart_data': chart_data
    }

    return render(request, 'mainapp/management_panel.html', context)