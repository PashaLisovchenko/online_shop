from django.db import models
from shop.models import Product
from decimal import Decimal


class Cart(models.Model):
    products = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField(default=1)
    product_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        if not self.product_price or self.product_price < self.products.price * self.quantity:
            self.product_price = self.products.price * self.quantity
        super(Cart, self).save(*args, **kwargs)


def get_total_price():
    cart = Cart.objects.all()
    prices = []
    for c in cart:
        prices.append(c.product_price)
    return sum(price for price in prices)
