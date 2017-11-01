from .models import Category, Product
from django.views.generic import ListView, DetailView
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class ProductList(ListView):
    template_name = 'list.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        category = None
        categories = Category.objects.all()
        products = Product.available_true.all()
        context['category'] = category
        context['categories'] = categories
        context['products'] = products
        return context


@method_decorator(login_required, name='dispatch')
class ProductListByCategory(DetailView):
    template_name = 'list.html'
    model = Category
    context_object_name = 'category'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        context = super(ProductListByCategory, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        products = Product.available_true.filter(category=context['category'])
        context['categories'] = categories
        context['products'] = products
        return context


@method_decorator(login_required, name='dispatch')
class ProductDetail(DetailView):
    template_name = 'detail.html'
    model = Product
    context_object_name = 'product'
    pk_url_kwarg = 'id'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context['cart_product_form'] = cart_product_form
        return context
