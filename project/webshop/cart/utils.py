from .models import Cart

def get_or_set_cart(request):
    try:
        cart = Cart.objects.get(customer_id=request.user)
    except:
        cart = Cart()
        cart.customer_id = request.user
        cart.save()
    return cart