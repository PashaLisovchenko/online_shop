from django.db import models
from account.models import User
from shop.models import Product


class Cart(models.Model):
    products = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField(default=1)
    product_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    user = models.ForeignKey(User, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.product_price = self.products.price * self.quantity
        super(Cart, self).save(*args, **kwargs)
