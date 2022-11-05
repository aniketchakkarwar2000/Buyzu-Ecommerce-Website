from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from product.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from coupons.forms import*
from product.models import Wishlist
@login_required
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']
        override = cd['override']
        cart.add(product=product,
            quantity=quantity,
            override_quantity=override)
        

    return redirect('cart:cart_detail')

@login_required
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

@login_required
def cart_detail(request):
    cart = Cart(request)
    print(cart)
    l = Wishlist.objects.filter(watchuser = request.user).values('product')
    x = [d['product'] for d in l if 'product' in d]
    
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})

    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html', {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form,
        'wlist':x,
        })
















