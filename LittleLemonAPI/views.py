from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer
from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from .permissions import IsManager, IsOwnerOrReadOnly

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
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            group, created = Group.objects.get_or_create(name='Manager')
            user.groups.add(group)
            return Response(status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class ManagerGroupUserDetailView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(name='Manager')
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
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'delivery_crew']
    ordering_fields = ['date', 'total']
    search_fields = ['date', '']
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        order = self.get_object()
        if order.user != request.user:
            return Response({'detail': 'You do not have permission to update this order.'}, status=403)
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        if order.user != request.user:
            return Response({'detail': 'You do not have permission to update this order.'}, status=403)
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        if order.user != request.user:
            return Response({'detail': 'You do not have permission to delete this order.'}, status=403)
        return super().delete(request, *args, **kwargs)