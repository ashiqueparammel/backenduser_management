from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth.models import AbstractUser
from users.models import CustomUser 

class UserRegister(serializers.ModelSerializer):
    
    password2 =serializers.CharField(style={'input_type':'password'},write_only=True)
    
    class Meta:
        model =CustomUser
        fields =["username","password","password2","email","profile_image"]
        # fields =["username","password","email","password2","first_name","last_name"]
    
    def save(self):
        reg=CustomUser(
            email =self._validated_data['email'],
            username=self._validated_data['username'],
            # first_name=self._validated_data['first_name'],
            # last_name=self._validated_data['last_name'],
            
        ) 
        password =self._validated_data['password'] 
        password2 =self._validated_data['password2']  
        if password!=password2:
            raise serializers.ValidationError({'password':'password does not match'})
        reg.set_password(password)
        reg.save()
        return reg 
    
class userDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =CustomUser
        fields =['id','username','email','first_name','last_name','profile_image']
        
class myTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_admin'] = user.is_superuser
        

        return token
        
    
    