from django.db import models
from mint_app.models import User, MModel


class CartQuerySet(models.QuerySet):
    def total_price(self):
        return sum([cart.products_price() for cart in self])

    def total_quantity(self) -> int:
        if self:
            return sum([cart.quantity for cart in self])
        return 0


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Пользователь")
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Стоимость')
    is_paid = models.BooleanField(default=False)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.user} | Сумма {self.price} | Оплачен {self.is_paid} | Дата {self.created_timestamp}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(to=MModel, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Заказ")

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        return f"Корзина {self.user} | Товар {self.product} | Количество {self.quantity}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    objects = CartQuerySet().as_manager()
