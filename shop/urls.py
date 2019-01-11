from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProductsList.as_view(), name="product_all"),
    path('product/<slug:slug>/', views.ProductView.as_view(), name='product'),
]