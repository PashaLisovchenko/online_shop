from django.test import TestCase
from django.urls import reverse
from .models import Category, Product
from django.utils.text import slugify
from cart.forms import CartAddProductForm


class ProductTest(TestCase):

    def create_product(self):
        name_category = 'Beverages'
        name_product = 'Fanta'
        category = Category.objects.create(name=name_category, slug=slugify(name_category))
        return Product.objects.create(category=category,
                                      name=name_product,
                                      slug=slugify(name_product),
                                      price=15.50,
                                      stock=20)

    def test_product_create(self):
        product = self.create_product()
        self.assertTrue(isinstance(product, Product))
        self.assertEqual(product.__str__(), product.name)

    def test_product_list_view(self):
        url = reverse('product_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['products'], [])

    def test_cart_quantity_valid_form(self):
        data = {'quantity': 1}
        form = CartAddProductForm(data=data)
        self.assertTrue(form.is_valid())

    def test_cart_quantity_invalid_form(self):
        data = {'quantity': 0}
        form = CartAddProductForm(data=data)
        self.assertFalse(form.is_valid())