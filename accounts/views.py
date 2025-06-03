from django.shortcuts import render
from rest_framework import generics,status
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate,login,logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from . import serializers
from . import models
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.conf import settings
# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        if user.is_active:
                return Response({'message': 'Account already verified.'}, status=status.HTTP_200_OK)
        
        token = default_token_generator.make_token(user)
        confirm_link = f'http://127.0.0.1:8000/api/auth/account/verify_email/{uid}/{token}/'

        # Send Email
        subject = 'Verify Your Email Account'
        from_email = settings.EMAIL_HOST_USER
        to_email = user.email
        html_content = render_to_string('verify_email.html', {
            'user': user,
            'confirm_link': confirm_link,
        })
        email = EmailMultiAlternatives(subject, '', from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        email.send()

        
        return Response({
            "message": "Account created successfully. Please check your email to verify your account.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }, status=status.HTTP_201_CREATED)
    
        
        
class AccountActivateView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = models.CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, models.CustomUser.DoesNotExist):
            return Response({'error': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({'message': 'Account already verified.'}, status=status.HTTP_200_OK)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            
            profile, created = models.Profile.objects.get_or_create(user=user)

            return Response({'message': 'Account verified successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired activation link.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):
    serializer_class = serializers.LoginSerializer
    
    def post(self,request,format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username,password=password)
            if not user:
                return Response({'error':'Invalid credentials.!'},status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            login(request,user)
            return Response({
                'refresh':str(refresh),
                'access':str(access),
                'message':'Login successful.',
                'user_role':user.user_role,
                'username': user.username
            },status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(APIView):
    def post(self,request):
        logout(request)
        return Response({'message':'Logout successful.'},status=status.HTTP_200_OK)

class PassChangeView(APIView):
    serializer_class = serializers.PassChangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,format=None):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        if serializer.is_valid():
            
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']
            user = request.user
            
            if new_password != confirm_password:
                return Response({'error':'new_password and confirm_password does not match.'},status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.save()
            return Response({'message':'Your password change successful.'},status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class PasswordResetView(APIView):
    serializer_class = serializers.PasswordResetSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if not models.CustomUser.objects.filter(email=email).exists():
                return Response({'error':'User not found with this email'},status=status.HTTP_400_BAD_REQUEST)
            
            user = models.CustomUser.objects.get(email=email)
            
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f'http://127.0.0.1:8000/api/auth/account/reset_pass/{uid}/{token}/'
            
            subject = 'Reset your Password'
            from_email = 'rakibulislamarif793@gmail.com'
            to_email = email
            html_content = render_to_string('reset_pass.html',{
                'user':user,
                'reset_link':reset_link,
            })
            email = EmailMultiAlternatives(subject,'',from_email,[to_email])
            email.attach_alternative(html_content,"text/html")
            email.send()
            return Response({'message':'Please check your email and reset your password.'})
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SetResetPasswordView(APIView):
    serializer_class = serializers.SetResetPasswordSerializer
    def post(self,request,uidb64,token):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['new_password']
            uid = urlsafe_base64_decode(uidb64).decode()
            user = models.CustomUser.objects.get(pk=uid)
            if user and default_token_generator.check_token(user,token):
                user.set_password(password)
                user.save()
                return Response({'message':'Your password reset successful.'},status=status.HTTP_200_OK)
            return Response({'error':'Invalid or expired your link'},status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ProfileUpdateSerializer
    def get(self,request):
        profile, created = models.Profile.objects.get_or_create(user=request.user)
        serializer = serializers.ProfileUpdateSerializer(profile,context={'request':request})
        return Response(serializer.data)

    def put(self,request):
        profile, created = models.Profile.objects.get_or_create(user=request.user)
        serializer = self.serializer_class(profile,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Profile update successful','data':serializer.data})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


class AllUserViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = models.CustomUser.objects.all()
    filter_backends = [DjangoFilterBackend,SearchFilter]
    search_fields = ['user_role']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.UserCreateByAdmin
        
        return serializers.AllUserSerializer