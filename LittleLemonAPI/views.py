from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer
from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from .permissions import IsManager, IsOwnerOrReadOnly, OnlyManager, OrdersPermission

# Menu-Item
class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsManager]
    filterset_fields = ['category', 'featured']
    ordering_fields = ['title', 'price']
    search_fields = ['title']

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsManager]

# User Management
    
class ManagerGroupUsersView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, OnlyManager]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')

        if not username:
            return Response({'detail': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Try to get the user by username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        group, _ = Group.objects.get_or_create(name='Manager')
        user.groups.add(group)

        return Response({"message": "user added to the manager group"},status=status.HTTP_201_CREATED)
        

class ManagerGroupUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, OnlyManager]

    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(name='Manager')
            user.groups.remove(group)
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class DeliveryGroupUsersView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Delivery Crew')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, OnlyManager]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')

        if not username:
            return Response({'detail': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Try to get the user by username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        group, _ = Group.objects.get_or_create(name='Delivery Crew')
        user.groups.add(group)

        return Response(status=status.HTTP_201_CREATED)

class DeliveryGroupUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(groups__name='Delivery Crew')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, OnlyManager]

    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(name='Delivery Crew')
            user.groups.remove(group)
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class CartListView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        Cart.objects.filter(user=user).delete()
        return Response(status=204)
    

class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, OrdersPermission]
    filterset_fields = ['status', 'delivery_crew']
    ordering_fields = ['date', 'total']
    search_fields = ['date', '']



    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        
        if user.groups.filter(name='Delivery Crew').exists():
            orders = Order.objects.filter(delivery_crew=user)
            return orders

        orders = Order.objects.filter(user=user)
        return orders


    def perform_create(self, serializer):
    # Get current user and their cart items
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            return Response({'detail': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        total = sum(item.price for item in cart_items)
        order = Order.objects.create(user=user, delivery_crew=None, status=False, date=self.request.data['date'], total=total)

        # Create order items from cart items
        for cart_item in cart_items:
            order_item_data = {
                'order': order.pk,
                'menuitem': cart_item.menuitem.id,
                'quantity': cart_item.quantity,
                'unit_price': cart_item.unit_price,
                'price': cart_item.price,
            }
            order_item_serializer = OrderItemSerializer(data=order_item_data)
            order_item_serializer.is_valid(raise_exception=True)
            order_item_serializer.save()

        # Delete cart items after creating order items
        cart_items.delete()

        # Update the total in the order
        order.total = order.calculate_total()
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, OrdersPermission]

    def put(self, request, *args, **kwargs):
        order = self.get_object()
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'detail': 'You do not have permission to update this order.'}, status=403)
        return super().put(request, *args, **kwargs)
    

    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()

        # Check if the request body contains 'status' key
        if 'status' not in request.data:
            return Response({'detail': 'Invalid request. Missing "status" key.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the value of 'status'
        new_status = request.data['status']
        if new_status not in [0, 1]:
            return Response({'detail': 'Invalid status value. Use 0 or 1.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the order status
        if request.user.groups.filter(name='Manager').exists():
            order.delivery_crew = request.data['delivery_crew']

        order.status = new_status
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        if order.user != request.user and not request.user.groups.filter(name='Manager').exists():
            return Response({'detail': 'You do not have permission to delete this order.'}, status=403)
        return super().delete(request, *args, **kwargs)