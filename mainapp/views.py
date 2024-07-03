from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView,UpdateView
from mainapp.models import Product, Order, Storage, OrderProduct
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay


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
    products = Product.objects.all()
    sales_data = {}

    for product in products:
        daily_sales = OrderProduct.objects.filter(product=product).annotate(day=TruncDay('order__order_date')).values('day').annotate(total_sales=Sum('quantity')).order_by('day')
        sales_data[product.name] = {
            'labels': [entry['day'].strftime('%Y-%m-%d') for entry in daily_sales],
            'data': [entry['total_sales'] for entry in daily_sales]
        }

    context = {
        'sales_data': sales_data
    }
    return render(request, 'mainapp/management_panel.html', context)