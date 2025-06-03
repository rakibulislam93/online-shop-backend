from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('all_user',views.AllUserViewset)

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('verify_email/<uidb64>/<token>/',views.AccountActivateView.as_view(),name='verify_email'),
    path('login/',views.LoginApiView.as_view(),name='login'),
    path('logout/',views.LogoutApiView.as_view(),name='logout'),
    path('pass_change/',views.PassChangeView.as_view(),name='pass_change'),
    path('reset_pass/',views.PasswordResetView.as_view(),name='reset_pass'),
    path('reset_pass/<uidb64>/<token>/',views.SetResetPasswordView.as_view(),name='set_resest_pass'),
    path('profile_update/',views.ProfileUpdateView.as_view(),name='profile_update'),
    
    path('',include(router.urls)),
]
