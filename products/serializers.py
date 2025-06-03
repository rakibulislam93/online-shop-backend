from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

    def update(self, instance, validated_data):
        icon = validated_data.get('icon',None)
        if icon is None:
            validated_data['icon'] = instance.icon
        return super().update(instance, validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.username',read_only=True)
    rating_display = serializers.SerializerMethodField()
    class Meta:
        model = models.Review
        fields = ['id','product','comment','rating','reviewer_name','rating_display']
    
    def get_rating_display(self,obj):
        return obj.get_rating_display()
    
    def validate(self, data):
        user = self.context['request'].user
        product = data.get('product')
        
        if not models.OrderItem.objects.filter(product=product,order__user=user,order__is_paid=True).exists():
            
            raise serializers.ValidationError({'error': 'You can not review before buying this product!'})
        
        if models.Review.objects.filter(product=product, reviewer=user).exists():
            raise serializers.ValidationError({'error':'You have already review this product.!'})
        
        return data



class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    created_by = serializers.CharField(read_only=True)
    reviews = ReviewSerializer(many=True,read_only=True)
    class Meta:
        model = models.Product
        fields = '__all__'
    
    
    def update(self, instance, validated_data):
        image = validated_data.get('image',None)
        if image is None:
            validated_data['image'] = instance.image
        return super().update(instance, validated_data)
        
    
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
    queryset=models.Product.objects.all(),
    source='product',
    write_only=True
)
    
    class Meta:
        model = models.CartItem
        fields = ['id','product','product_id','quantity','created_at','updated_at']
        
    
    def create(self, validated_data):
        user = self.context['request'].user
        cart, _ = models.Cart.objects.get_or_create(user=user)
        product = validated_data['product']
        
        quantity = validated_data.get('quantity',1)
        
        cart_item, created = models.CartItem.objects.get_or_create(cart=cart,product=product)
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
            
        cart_item.save()
        
        return cart_item
        

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    class Meta:
        model = models.Cart
        fields = ['id','user','created_at','updated_at','items']
        
    
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = models.OrderItem
        fields = ['id','product','quantity','price','created_at']
    
    
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True,read_only=True)
    username = serializers.CharField(source="user.username",read_only=True)
    class Meta:
        model = models.Order
        fields = ['id','user','username','total_price','is_paid','status','created_at','order_items']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        
        # customer can change only cancel
        if user.user_role == 'customer':
            if 'status' in validated_data and validated_data['status'] != 'cancelled':
                raise serializers.ValidationError("You are not allowed to change the status except to Cancel ")
        
        # seller can change status but not change is_paid
        elif user.user_role == 'seller':
            validated_data.pop('is_paid',None)
        
        # admin can anything..
        return super().update(instance,validated_data)




        