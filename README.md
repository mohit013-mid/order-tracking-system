Real-Time Order Tracking System

A real-time order management system built with:

Django

Django REST Framework

Django REST Framework SimpleJWT

Django Channels

Websockets

1. Authentication

JWT-based authentication

Access & Refresh token support

Role-based login (Admin, Customer, Agent)

2. Dashboards

Admin dashboard

Customer dashboard

Agent dashboard

3. Order Management

Create orders

Assign agents to orders

Track order status

4. Real-Time Updates

Order status updates delivered via WebSockets

Secure WebSocket connections using JWT authentication


5. FLOW 
CUSTOMER CREATE ORDERS 
ORDER REQUEST  GO TO ADMIN 
THEN ADMIN ASSIGN THE DELIVERY AGENT TO THE ORDER 
DELIVERY AGENT SEE THE ORDER REQUEST 
IF DELIVERY AGENT CHANGE THE STATUS OF ORDER IN REAL TIME STATUS IS UPDATES IN THE CUSTOMER DASHBOARD 
