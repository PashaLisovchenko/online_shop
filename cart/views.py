from django.db.models import Sum
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin
from shop.models import Product
from .models import Cart
from .forms import CartAddProductForm
from django.views.generic import DeleteView, ListView, CreateView, DetailView


@login_required
def get_total_price(request):
    total = Cart.objects.filter(user=request.user).aggregate(total_sum=Sum('product_price'))
    if total['total_sum']:
        return total['total_sum']
    return 0


@login_required
def get_total_item(request):
    total_quantity = Cart.objects.filter(user=request.user).aggregate(total_sum=Sum('quantity'))
    if total_quantity['total_sum']:
        return total_quantity['total_sum']
    return 0


@method_decorator(login_required, name='dispatch')
class CartDetail(FormMixin, ListView):
    model = Cart
    form_class = CartAddProductForm
    template_name = 'detail_card.html'
    context_object_name = 'cart'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CartDetail, self).get_context_data(**kwargs)
        context['get_total_price'] = get_total_price(self.request)
        for item in context['cart']:
            item.quantity = CartAddProductForm(
                initial={'quantity': item.quantity})
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
        cart = Cart.objects.filter(products__name=self.object.name)

        if cart.exists():
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


@method_decorator(login_required, name='dispatch')
class CardUpdate(FormMixin, DetailView):
    model = Cart
    form_class = CartAddProductForm
    pk_url_kwarg = 'cart_id'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = self.get_object()
        cart = Cart.objects.get(products=self.object.products)
        cd = form.cleaned_data
        cart.quantity = cd['quantity']
        cart.save()
        return redirect('cart:cart_detail')

