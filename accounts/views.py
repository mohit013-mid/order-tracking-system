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



class registerView(APIView):

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

        return Response({
            "message": "User created"
        })


class LoginView(APIView):

    permission_classes = [AllowAny]

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
        login(request, user)

        # create JWT
        refresh = RefreshToken.for_user(user)

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

    return Response({
        "message": "Agent assigned successfully",
        "order_id": order.id,
        "agent": agent.username,
        "status": order.status   # unchanged
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
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


def admin_dashboard(request):

    orders = Order.objects.all()

    agents = Profile.objects.filter(role="AGENT")

    return render(request,"admin-dashboard.html",{
        "orders": orders,
        "agents": agents
    }) 

@login_required(login_url="/login-page/")
def customer_dashboard(request):
    products = Product.objects.all()
    return render(request, "customer-dashboard.html", {
        "products": products
    })  


def customer_order(request):
    return render(request, "cus-order.html")


def admin_products(request):
    products = Product.objects.all()
    return render(request, "admin_product.html",{"products":products})


def agent_dashboard(request):
    return render(request, "agent-dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("/api/auth/login-page/")