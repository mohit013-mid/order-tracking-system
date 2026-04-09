from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate , login , logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
from .models import Product
from ordersystem.models import Order  , OrderAssignment
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny
from notification.services import notify_admins , notify_user


class registerView(APIView):
    permission_classes = [AllowAny]

    

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")
        role = request.data.get("role")

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Profile.objects.create(
            user=user,
            role=role
        )


        # 🔔 SEND EVENTS HERE

        # 👑 Notify admins
        notify_admins(f"New user registered: {username}")

        # 👤 Notify user (optional)
        notify_user(user, "Welcome! Your account has been created.")

        return Response({
            "message": "User created"
        })
    def get(self, request):
        return render(request, "register.html")
    



class LoginView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
            return render(request, "login.html")


    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # create Django session
        # login(request, user)

        # create JWT tokens
        refresh = RefreshToken.for_user(user)
        #print("refresh token", str(refresh))
        #print("access token", str(refresh.access_token))

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username,
            "role": user.profile.role
        })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def assign_agent(request):

    order_id = request.data.get("order_id")
    agent_id = request.data.get("agent_id")

    order = Order.objects.get(id=order_id)
    agent = User.objects.get(id=agent_id)

    # assign agent only
    order.agent = agent
    order.save()

    OrderAssignment.objects.update_or_create(
        order=order,
        defaults={"agent": agent}
    )
    print("assign user is", request.user)
    print("order is ", order_id)
    print("agent is ", agent)
    print("agent is ", agent.id)
    # 🔔 SEND EVENTS HERE

    # 👑 Notify admins
    notify_admins(f"you have succesfully assign order with order id  {order_id} to {agent}")

    # # 👤 Notify user (optional)
    notify_user(agent, f"Welcome! Your have recieved new order {order.id}.")
    
    return Response({
        "message": "Agent assigned successfully",
        "order_id": order.id,
        "agent": agent.username,
        "status": order.status   # unchanged
    })

@api_view(["GET"])
def agent_assigned_orders(request):

    permission_classes = [IsAuthenticated]

    assignments = OrderAssignment.objects.select_related(
        "order",
        "order__customer",
        "order__product"
    ).filter(agent=request.user)

    orders_data = []

    for assignment in assignments:

        order = assignment.order

        orders_data.append({
            "order_id": order.id,
            "customer": order.customer.username,
            "product": order.product.name,
            "status": order.status,
            "created_at": order.created_at,
            
        })

    return Response(orders_data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer_orders_api(request):

    orders = Order.objects.filter(customer=request.user).select_related("product")

    data = []

    for order in orders:
        data.append({
            "id": order.id,
            "product": order.product.name,
            "status": order.status,
            "created_at": order.created_at
        })

    return Response(data)

def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")



# def admin_dashboard(request):
#     print("user9999999999999999999999", request.user)
    
#     permission_classes = [IsAuthenticated]
#     orders = Order.objects.all()

#     agents = Profile.objects.filter(role="AGENT")

#     return render(request,"admin-dashboard.html",{
#         "orders": orders,
#         "agents": agents
#     }) 
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def admin_dashboard_api(request):

    # 🔒 Optional: Only allow ADMIN
    if request.user.profile.role != "ADMIN":
        return Response({"error": "Permission denied"}, status=403)

    orders = Order.objects.select_related("customer", "product", "agent")
    agents = Profile.objects.filter(role="AGENT").select_related("user")

    orders_data = []
    for order in orders:
        orders_data.append({
            "id": order.id,
            "customer": order.customer.username,
            "product": order.product.name,
            "agent": order.agent.username if order.agent else None,
            "status": order.status,
            "created_at": order.created_at
        })

    agents_data = []
    for agent in agents:
        agents_data.append({
            "id": agent.user.id,
            "username": agent.user.username
        })

    return Response({
        "orders": orders_data,
        "agents": agents_data
    })
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Product
from .serializers import ProductSerializer


class AdminProductView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # required for image upload

    def get(self, request):
        """List all products"""
        products = Product.objects.all().order_by("-created_at")
        serializer = ProductSerializer(products, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Add a new product"""

        # Only admins can add products
        if request.user.profile.role != "ADMIN":
            return Response(
                {"error": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Product added successfully.", "product": serializer.data},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, product_id):
        """Delete a product"""

        if request.user.profile.role != "ADMIN":
            return Response(
                {"error": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return Response(
                {"message": "Product deleted successfully."},
                status=status.HTTP_200_OK
            )
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )


def customer_dashboard(request):
    print("userrr", request.user)
    products = Product.objects.all()
    return render(request, "customer-dashboard.html", {
        "products": products
    })


def customer_order(request):
    print("userrrrrrrrrrrr", request.user)
    
    return render(request, "cus-order.html")


def admin_products(request):
    products = Product.objects.all()
    return render(request, "admin_product.html" )

def admin_dashboard(request):
    return render(request,"admin-dashboard.html")

def agent_dashboard(request):
    return render(request, "agent-dashboard.html")


def logout_view(request):
    print("logout")
    logout(request)
    return redirect("/api/auth/login-page/")