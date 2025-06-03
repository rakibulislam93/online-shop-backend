from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('list',views.ProductView)
router.register('category',views.CategoryView)
router.register('reviews',views.ReviewViewset)
router.register('my-products',views.ProductViewRoleWise,basename='my-products')

urlpatterns = [
    path('',include(router.urls)),
    path('cart/',views.CartView.as_view()),
    path('cart/add/',views.AddToCartView.as_view()),
    path('cart/remove/<int:pk>/', views.RemoveFromCartView.as_view()),
    path('cart/clear/',views.ClearAllFromCartView.as_view(),name='clear_cart'),
    path('checkout/', views.CheckoutView.as_view()),
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/',views.OrderUpdateView.as_view(),name='order_update'),
    path('seller_orders/',views.SellerOwnProductOrder.as_view(),name='sellerOwn_product_orders'),
    
    # only create for request to the server..after 14 minitue auto run it..
    path('test_request/',views.test.as_view(),name='test_request')
    
]
