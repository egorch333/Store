from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProductsList.as_view(), name="product_all"),
    path('detail/<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
    path("add-cartitem/<slug:slug>/<int:pk>/", views.AddCartItem.as_view(), name="add_cartitem"),
    path("cart/", views.CartItemList.as_view(), name="cart_item"),
    path("delete/<int:pk>/", views.RemoveCartItem.as_view(), name="del_item"),
    path("edit/<int:pk>/", views.EditCartItem.as_view(), name="edit_item"),
    path("add_order/", views.AddOrder.as_view(), name="add_order"),
    path("orders/", views.OrderItemList.as_view(), name="order_item"),
]