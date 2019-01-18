from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProductsList.as_view(), name="product_all"),
    path('detail/<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
    path("add-cartitem/<slug:slug>/<int:pk>/", views.AddCartItem.as_view(), name="add_cartitem"),
    path("cart/", views.CartItemList.as_view(), name="cart_item"),
    path("edit-cart/<int:pk>/<slug:slug>/<int:price>/", views.CartItemEdit.as_view(), name="edit_cart"),
]