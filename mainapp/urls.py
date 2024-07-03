from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='index'),
    path('create_product/', views.ProductCreateView.as_view(), name='create_product'),
    path('store/', views.store_view, name='store'),
    path('management/', views.management_panel, name='management_panel'),
    path('select_storage/', views.select_storage_view, name='select_storage'),
    path('update_storage/<int:pk>',views.StorageUpdateView.as_view(),name='update_storage'),
]
