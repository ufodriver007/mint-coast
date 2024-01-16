from django.urls import path, include
from cart.views import CartIndexView, AddToCartView, DeleteCart, DeleteCartItem, AddCartItem, CreateCartFast


urlpatterns = [
    path('', CartIndexView.as_view(), name='cart'),
    path('<int:model_id>/', CreateCartFast.as_view()),
    path('add/<int:model_id>/', AddToCartView.as_view()),
    path('delete/<int:product_id>/', DeleteCart.as_view()),
    path('delete/item/<int:product_id>/', DeleteCartItem.as_view()),
    path('add/item/<int:product_id>/', AddCartItem.as_view()),
]
