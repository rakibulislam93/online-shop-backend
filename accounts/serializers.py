from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from . import models

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = models.CustomUser
        fields = ['id','username','email','password','confirm_password','user_role']
        extra_kwargs = {
            'password':{'write_only':True},
        }
    
    def validate_email(self,value):
        if not value.endswith('.com'):
            raise serializers.ValidationError({'error':'Only .com domain allowed'})
        return value
    
    def validate_password(self,value):
        if len(value) < 8:
            raise serializers.ValidationError({'error':'Password must be at least 8 characters long.'})
        validate_password(value)
        
        return value
    
    def validate(self, data):
        
        password1 = data.get('password')
        password2 = data.get('confirm_password')
        
        if password1 != password2:
            raise serializers.ValidationError({'error':'password and confirm password does not match'})
        return data

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        password = validated_data['password']
        user = models.CustomUser(**validated_data)
        user.is_active = False
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class PassChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()
    
    def validate(self,data):
        user = self.context['request'].user
        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError({'error':'Your old password does not match.!'})
        
        return data
    
    def validate_new_password(self,value):
        validate_password(value)
        return value

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class SetResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    
    def validate_new_password(self,value):
        if len(value) < 8:
            raise serializers.ValidationError({'error':'Password must be at least 8 characters long.'})
        validate_password(value)
        
        return value


class ProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = models.Profile
        fields =['id','username','email','profile_pic','address','phone']
        

# show for all user 
class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['id','username','email','is_active','user_role','approval_status','is_staff']
        read_only_fields = ['username','email']

# create a new user by admin
class UserCreateByAdmin(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['username','email','password','is_active','user_role','approval_status','is_staff']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = models.CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user