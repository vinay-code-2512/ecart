from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mainApp.models import Product
from .serializers import ProductSerializer
from django.contrib.auth.models import User
from mainApp.models import Buyer
from rest_framework import status
from django.contrib.auth import authenticate
from mainApp.models import Checkout, CheckoutProducts, Buyer


@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def signup_api(request):
    #this gets what user write in username ex: vikrant
    username = request.data.get("username") 
    password = request.data.get("password")
    name = request.data.get("name")
    email = request.data.get("email")
    phone = request.data.get("phone")

    if username is None or password is None:
        return Response({"error":"Username and password required"}, status=400)
    
    # User => is a model class, Each row= one user
    # .objects => Gateway to DB.Think of it as a remote control for the table.It allows you to:Fetch data,Insert data,Update data,Delete data from database table
    # .filter() => Search rows matching a condition  
    if User.objects.filter(username=username).exists():
        return Response({"error":"Username already exists"}, status=400)
    
    # Create user object in memory and hash password(encrypted password)
    user = User(username=username)
    user.set_password(password)
    user.save()

    buyer = Buyer(
        username=username,
        name=name,
        email=email,
        phone=phone
    )
    buyer.save()
    return Response({"message":"Account created successfully"})


@api_view(['POST'])
def login_api(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({"error":"Username and password required"}, status=400)
    
    # Return user object if credentials are correct and None if incorrect
    user = authenticate(username=username, password=password)
    if user != None:
        return Response({"message":"Login successful"})
    else:
        return Response({"error":"Invalid username or password"}, status=401)
    

@api_view(['POST'])
def add_to_cart_api(request):
    # Extract product_id(ex : 5)
    product_id = request.data.get("product_id")

    try:
        # Fetches product whose id = product_id
        p = Product.objects.get(id=product_id)
    except:
        return Response({"error":"Product not found"}, status=404)
 
    #Looks inside session for cart. 
    # If none exists, creates empty dictionary {}
    cart = request.session.get("cart", {})
    
    #We convert product_id to string because session stores dictionary keys as strings.
    if str(product_id) in cart:
        # Nested dictionary update
        cart[str(product_id)]["qty"] += 1
        cart[str(product_id)]["total"] += p.finalprice
    else:
        cart[str(product_id)] = {
            "id": p.id,
            "name": p.name,
            "price": p.finalprice,
            "qty": 1,
            "total": p.finalprice
        }
    
    # Calculation for all products in cart
    subtotal = 0
    count = 0

    for item in cart.values():
        subtotal += item["total"]
        count += item["qty"]

    shipping = 150 if subtotal < 1000 and subtotal > 0 else 0
    total = subtotal + shipping

    # To store cart in session 
    # key="cart" , value=cart(dictionary)
    request.session["cart"] = cart
    request.session["subtotal"] = subtotal
    request.session["shipping"] = shipping
    request.session["total"] = total
    request.session["count"] = count

    return Response({
        "message": "Item added to cart",
        "cart": cart,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total
    })


# This API only reads data
@api_view(['GET'])
def view_cart_api(request):

    # .get("cart", {}) => Find key named "cart" OR it retrieves cart
    cart = request.session.get("cart", {})
    subtotal = request.session.get("subtotal", 0)
    shipping = request.session.get("shipping", 0)
    total = request.session.get("total", 0)
    count = request.session.get("count", 0)

    return Response({
        "cart": cart,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
        "count": count
    })


@api_view(['POST'])
def remove_from_cart_api(request):
    product_id = request.data.get("product_id")
    cart = request.session.get("cart", {})

    if str(product_id) not in cart:
        return Response({"error": "Item not in cart"}, status=404)

    # Remove item
    del cart[str(product_id)]

    # Recalculate
    subtotal = 0
    count = 0
    for item in cart.values():
        subtotal += item["total"]
        count += item["qty"]

    shipping = 150 if subtotal < 1000 and subtotal > 0 else 0
    total = subtotal + shipping

    # To store cart in session 
    # key="cart" , value=cart(dictionary)
    request.session["cart"] = cart
    request.session["subtotal"] = subtotal
    request.session["shipping"] = shipping
    request.session["total"] = total
    request.session["count"] = count

    return Response({
        "message": "Item removed",
        "cart": cart,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
        "count": count
    })


@api_view(['POST'])
def update_cart_qty_api(request):
    product_id = request.data.get("product_id")
    operation = request.data.get("operation")  # inc or dec
    
    # .get("cart", {}) => Find key named "cart" OR it retrieves cart
    cart = request.session.get("cart", {})

    if str(product_id) not in cart:
        return Response({"error": "Item not in cart"}, status=404)

    item = cart[str(product_id)]
    price = item["price"]

    if operation == "inc":
        item["qty"] += 1
        item["total"] += price

    elif operation == "dec":
        if item["qty"] == 1:
            return Response({"error": "Minimum quantity is 1"}, status=400)
        item["qty"] -= 1
        item["total"] -= price

    else:
        return Response({"error": "Invalid operation"}, status=400)

    # Recalculate totals
    subtotal = 0
    count = 0
    for i in cart.values():
        subtotal += i["total"]
        count += i["qty"]

    shipping = 150 if subtotal < 1000 and subtotal > 0 else 0
    total = subtotal + shipping
    
    # To store cart in session 
    # key="cart" , value=cart(dictionary)
    request.session["cart"] = cart
    request.session["subtotal"] = subtotal
    request.session["shipping"] = shipping
    request.session["total"] = total
    request.session["count"] = count

    return Response({
        "message": "Quantity updated",
        "cart": cart,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
        "count": count
    })


@api_view(['POST'])
def checkout_api(request):
    username = request.data.get("username")
    payment_mode = request.data.get("payment_mode")  # COD or ONLINE

    if not username:
        return Response({"error": "Username required"}, status=400)

    try:
        buyer = Buyer.objects.get(username=username)
    except:
        return Response({"error": "Buyer not found"}, status=404)

    cart = request.session.get("cart", {})

    if not cart:
        return Response({"error": "Cart is empty"}, status=400)

    subtotal = request.session.get("subtotal", 0)
    shipping = request.session.get("shipping", 0)
    total = request.session.get("total", 0)
    
    # Create Checkout
    # Creates a new order record(id) in the database and stores it inside variable "check".
    # .objects => database ke sath baat krne ka tool
    # .create => Creates a new row in database and saves it automatically.
    check = Checkout.objects.create(
        buyer=buyer,
        subtotal=subtotal,
        shipping=shipping,
        final=total
    )

    # Create CheckoutProducts
    # Products in checkout
    for item in cart.values():
        CheckoutProducts.objects.create(
            checkout=check,
            product_id=item["id"],
            qty=item["qty"],
            total=item["total"]
        )


    if payment_mode == "COD":
        check.paymentMode = 1
        check.save()
        
        # Clear cart only for COD
        request.session["cart"] = {}
        request.session["subtotal"] = 0
        request.session["shipping"] = 0
        request.session["total"] = 0
        request.session["count"] = 0

        return Response({
            "message": "Order placed successfully",
            "order_id": check.id,
            "payment_mode": "COD"
        })

    else:
        check.paymentMode = 2
        check.save()
        return Response({
            "message": "Proceed to online payment",
            "order_id": check.id,
            "payment_mode": "ONLINE"
        })
    

@api_view(["POST"])
def payment_success(request):
    request.session["cart"] = {}
    request.session["subtotal"] = 0
    request.session["shipping"] = 0
    request.session["total"] = 0
    request.session["count"] = 0

    return Response({"message": "Payment successful"})
