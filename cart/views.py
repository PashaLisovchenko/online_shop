from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin
from shop.models import Product
from .models import Cart, get_total_price
from .forms import CartAddProductForm
from django.views.generic import DeleteView, ListView, CreateView


@method_decorator(login_required, name='dispatch')
class CartDetail(FormMixin, ListView):
    model = Cart
    form_class = CartAddProductForm
    template_name = 'detail_card.html'
    context_object_name = 'cart'

    def get_context_data(self, **kwargs):
        context = super(CartDetail, self).get_context_data(**kwargs)
        context['get_total_price'] = get_total_price
        return context


@method_decorator(login_required, name='dispatch')
class CartRemove(DeleteView):
    model = Cart
    template_name = 'delete_product.html'
    pk_url_kwarg = 'cart_id'
    success_url = '/cart'


@method_decorator(login_required, name='dispatch')
class CardAdd(CreateView):
    model = Product
    form_class = CartAddProductForm
    pk_url_kwarg = 'product_id'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = self.get_object()
        print(self.object)
        cart = Cart.objects.all()
        product_name = []
        for c in cart:
            product_name.append(c.products.name)

        if self.object.name in product_name:
            cart = Cart.objects.get(products=self.object)
            cd = form.cleaned_data
            cart.quantity = cd['quantity'] + cart.quantity
            cart.save()
            return redirect('cart:cart_detail')
        else:
            cd = form.cleaned_data
            cd['products'] = self.object
            Cart.objects.create(**cd)
            return redirect('cart:cart_detail')

