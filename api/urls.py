from django.urls import path
from .views import checkout_api
from .views import payment_success

from .views import (
    product_list,
    signup_api,
    login_api,
    add_to_cart_api,
    view_cart_api,
    remove_from_cart_api,
    update_cart_qty_api
)

urlpatterns = [
    path("products/", product_list),
    path("signup/", signup_api),
    path("login/", login_api),
    path("add-to-cart/", add_to_cart_api),
    path("view-cart/", view_cart_api),
    path("remove-from-cart/", remove_from_cart_api),
    path("update-cart/", update_cart_qty_api),
    path("checkout/", checkout_api),
    path("payment-success/", payment_success),

]

