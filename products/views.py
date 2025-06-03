from django.shortcuts import render
from rest_framework import viewsets,status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import permissions
from . import models
from . import serializers
from .filters import ProductFilter
from django.shortcuts import get_object_or_404
# Create your views here.

class CategoryView(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsCustomerReadOnly | permissions.IsAdminOrSeller]
    
    
class ProductView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsCustomerReadOnly | permissions.IsAdminOrSeller]
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    # custom filter logic
    filterset_class = ProductFilter
    
    search_fields = ['name','title','description','category__name']
    
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProductViewRoleWise(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    search_fields = ['category__name','name']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return models.Product.objects.all()
        return models.Product.objects.filter(created_by=user)


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cart, _ = models.Cart.objects.get_or_create(user=request.user)
        serializer = serializers.CartSerializer(cart)
        return Response(serializer.data)

class AddToCartView(APIView):
    serializer_class = serializers.CartItemSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        if serializer.is_valid():
            
            serializer.save()
            
            return Response({'message':"Product added to cart"})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        cart = get_object_or_404(models.Cart, user=request.user)
        item = get_object_or_404(models.CartItem, id=pk, cart=cart)
        item.delete()
        return Response({'message': 'Item removed'}, status=status.HTTP_200_OK)

class ClearAllFromCartView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        cart, created = models.Cart.objects.get_or_create(user=request.user)
        
        if not cart.items.exists():
            return Response({'message': 'Your cart is already empty.'}, status=status.HTTP_200_OK)
        
        cart.items.all().delete()
        return Response({'message': 'All items removed from your cart.'},status=status.HTTP_200_OK)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        cart = get_object_or_404(models.Cart, user=request.user)
        cart_items = cart.items.all()
        if not cart_items:
            return Response({'message': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        for item in cart_items:
            if item.product.quantity < item.quantity:
                return Response({'message':'Not enough stock'},status=status.HTTP_400_BAD_REQUEST)
            
        
        total = sum(item.product.price * item.quantity for item in cart_items)
        order = models.Order.objects.create(user=request.user, total_price=total)

        for item in cart_items:
            models.OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.product.quantity -= item.quantity
            item.product.save()
        cart.items.all().delete()

        return Response({'message': 'Order placed successfully'}, status=status.HTTP_201_CREATED)


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.is_staff:
            orders = models.Order.objects.all().order_by('-created_at')
        else:
            orders = models.Order.objects.filter(user=user).order_by('-created_at')
        serializer = serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def has_permission_to_update(self,user,order):
        if user.is_staff:
            return True # admin all control
        
        elif any(item.product.created_by == user for item in order.order_items.all()):
            return True
        
        elif user == order.user and order.status == "pending":
            return True
        
        return False

    def patch(self,request,pk):
        try:
            order = models.Order.objects.get(pk=pk)
        except models.Order.DoesNotExist:
            return Response({'error':'Order not found'},status=status.HTTP_404_NOT_FOUND)
        
        if not self.has_permission_to_update(request.user,order):
            return Response({'error': 'You do not have permission to update this order'},status=status.HTTP_403_FORBIDDEN)
        
        serializer = serializers.OrderSerializer(order,data=request.data,partial=True,context={'request':request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class SellerOwnProductOrder(APIView):
    def get(self,request):
        user = request.user
        if user.user_role != 'seller':
            return Response({'detail':'Only sellers can access this.'},status=status.HTTP_403_FORBIDDEN)

        orders = models.Order.objects.filter(order_items__product__created_by=user).distinct().order_by('-created_at')
        
        serializer = serializers.OrderSerializer(orders,many=True)
        return Response(serializer.data)
        

class ReviewViewset(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)