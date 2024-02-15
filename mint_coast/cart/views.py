from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from cart.models import Cart, MModel
from urllib.parse import urlencode


class CartIndexView(View):
    def get(self, request, *args, **kwargs):
        carts = Cart.objects.filter(user=request.user).order_by("product")
        total_price = sum([cart.products_price() for cart in carts])

        get_parameters = {}
        for cart in carts:
            get_parameters[cart.id] = ''
        get_parameters = urlencode(get_parameters)
        return render(request, 'cart.html', context={'carts': carts, 'total_price': total_price, 'get_parameters': get_parameters})


class CreateCartFast(View):
    def get(self, request, model_id, *args, **kwargs):
        product = MModel.objects.get(id=model_id)

        if request.user.is_authenticated:
            if Cart.objects.filter(user=request.user, product=product).exists():
                return redirect('cart')
            else:
                cart = Cart.objects.create(user=request.user, product=product, quantity=1)
                cart.save()
                return redirect('cart')
        else:
            return redirect('home')


class AddToCartView(View):
    def post(self, request, model_id, *args, **kwargs):
        if request.user.is_authenticated:
            product = MModel.objects.get(id=model_id)

            if Cart.objects.filter(user=request.user, product=product).exists():
                cart = Cart.objects.get(user=request.user, product=product)
                cart.quantity += 1
                cart.save()
            else:
                cart = Cart.objects.create(user=request.user, product=product, quantity=1)
                cart.save()
            messages.info(request, f'В корзину добавлен товар {product.name}')
            return redirect(request.META['HTTP_REFERER'])


class DeleteCart(View):
    def post(self, request, product_id, *args, **kwargs):
        if request.user.is_authenticated:
            product = MModel.objects.get(id=product_id)
            cart = Cart.objects.get(user=request.user, product=product)
            cart.delete()
            messages.info(request, f'Из корзины удалён тип товара {product.name}')

            return redirect(request.META['HTTP_REFERER'])


class DeleteCartItem(View):
    def post(self, request, product_id, *args, **kwargs):
        if request.user.is_authenticated:
            product = MModel.objects.get(id=product_id)

            cart = Cart.objects.get(user=request.user, product=product)
            if cart.quantity:
                cart.quantity -= 1
                cart.save()
                messages.info(request, f'Из корзины удалён один товар {product.name}')

                return redirect(request.META['HTTP_REFERER'])


class AddCartItem(View):
    def post(self, request, product_id, *args, **kwargs):
        if request.user.is_authenticated:
            product = MModel.objects.get(id=product_id)

            cart = Cart.objects.get(user=request.user, product=product)
            if cart.quantity:
                cart.quantity += 1
                cart.save()
                messages.info(request, f'В корзину добавлен один товар {product.name}')

                return redirect(request.META['HTTP_REFERER'])
