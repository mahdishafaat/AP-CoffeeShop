from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView,UpdateView
from mainapp.models import Product, Order, Storage, OrderProduct
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict

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
    # Get today's date and calculate the date 7 days ago
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)
    dates = [start_date + timedelta(days=i) for i in range(7)]
    date_labels = [date.strftime("%Y-%m-%d") for date in dates]

    # Initialize sales data structure
    sales_data = defaultdict(lambda: {
        'labels': date_labels,
        'data': [0] * 7  # Initialize with zeros for each day of the week
    })

    # Query for all sales in the last week
    last_week_sales = OrderProduct.objects.filter(order__order_date__date__range=[start_date, end_date])

    # Populate sales data
    for sale in last_week_sales:
        product_name = sale.product.name
        sale_date = sale.order.order_date.date().strftime("%Y-%m-%d")
        if sale_date in sales_data[product_name]['labels']:
            index = sales_data[product_name]['labels'].index(sale_date)
            sales_data[product_name]['data'][index] += sale.quantity
    return render(request, 'mainapp/management_panel.html', {'sales_data': dict(sales_data)})