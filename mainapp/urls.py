from django.urls import path
from . import views
from mainapp.views import ProductCreateView,store_view

urlpatterns = [
    path('', views.homepage, name='index'),
    path('create_product/', ProductCreateView.as_view(), name='create product'),
    path('store/',store_view, name='store')
]
