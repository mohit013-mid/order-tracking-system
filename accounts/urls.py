from django.urls import path
from .views import assign_agent, register_page, registerView, LoginView,  login_page , agent_assigned_orders, current_user ,customer_orders_api
from .views import admin_dashboard, customer_dashboard, agent_dashboard, customer_order  , admin_products , logout_view , AdminProductView, admin_dashboard_api, current_user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # path("register/", register_view, name="register"),
    # # JWT login
    # path("login/", TokenObtainPairView.as_view(), name="login"),

    # refresh token
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", registerView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("current-user/", current_user , name="current_user"),
    # path("login-page/", login_page, name="login_page"),
    # path("register-page/", register_page, name="register_page"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard-api/", admin_dashboard_api),
    path("customer-dashboard/", customer_dashboard, name="customer_dashboard"),
    path("agent-dashboard/", agent_dashboard, name="agent_dashboard"),
    path("assign-agent/", assign_agent, name="assign_agent"),
    path("agent-orders/", agent_assigned_orders, name="agent_orders"),
    path("customer_order_api/", customer_orders_api, name="customer_order_api"),
    path("customerorder/", customer_order , name="customerorder"),
    path("admin_product", admin_products , name="admin_product"),
     path("admin_product_listing/",          AdminProductView.as_view(), name="admin_product"),
    path("admin_product/<int:product_id>/", AdminProductView.as_view(), name="admin_product_delete"),
    path("logout/", logout_view, name="logout")
]