from django.db import models
from shop.models import Product


class Cart(models.Model):
    products = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField(default=1)
    product_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        self.product_price = self.products.price * self.quantity
        super(Cart, self).save(*args, **kwargs)


def get_total_price():
    total = Cart.objects.annotate(total_sum=Sum('product_price'))
    if total.first():
        return total.first().total_sum
    return 0
