from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='index'),
    path('create_product/', views.ProductCreateView.as_view(), name='create product'),
    path('store/', views.store_view, name='store'),
    path('management/', views.management_panel, name='management_panel'),
]
