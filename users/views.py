from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from users.models import CustomUser
from users.serializers import UserRegister,userDataSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import myTokenObtainPairSerializer
from rest_framework.filters import SearchFilter
import json
# Create your views here.

class register(APIView):
    
    def post(self,request,format=None):
        serializer=UserRegister(data=request.data)
        check =request.data['email']
        if CustomUser.objects.filter(email=check).exists():
            text='email already exist!'
            data = {
            'text': text,
            'status': 404
            }
            return Response(data,status=404)
        
        
        if serializer.is_valid():
            data = {}
            
            account =serializer.save()
            data['response']='registerd'
            data['username']=account.username
            data['first_name']=account.first_name
            data['last_name']=account.last_name
            data['email']=account.email
            token,create=Token.objects.get_or_create(user=account)
            data['token']=token.key
        else:
            statusText = serializer.errors
            json_object = json.dumps(statusText)
            data = json.loads(json_object)
            text =data.get("username", [0])
            text =str(text[0])
            data = {
            'text': text,
            'status': 404
            }
            return Response(data,status=404)
           
        return Response(data)         
            
class home(APIView):
    permission_classes=(IsAuthenticated,)
    
    def get(self,request):
        content={'user':str(request.user),'userid':str(request.user.id),'email':str(request.user.email),'password':str(request.user.password)}
        return Response(content)  
        
    
class userDetails(APIView):
    # permission_classes=(IsAuthenticated,)
    
    def get_object(self,pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except:
            raise Http404
            # return Response({'message':'no user'})
        
    def get(self,request,pk,format=None):
        userData=self.get_object(pk)
        serializer=userDataSerializer(userData)  
        return Response(serializer.data)
    
    def put(self,request,pk,format=None):
        userData =self.get_object(pk)
        # datacheck =request.data
        # email=datacheck['email']
        
        # if CustomUser.objects.filter(email=email).exists():
        #     # print('checkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')    
        #     text='email already exist!'
        #     data = {
        #     'text': text,
        #     'status': 404
        #     }
        #     return Response(data )
           
        
        serializer=userDataSerializer(userData,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message':'error','error':serializer.errors})
    def patch(self,request,pk,format=None):
        userData =self.get_object(pk)
        datacheck =request.data
        print(datacheck,'checkkkkkkkkkkkkkkkkkkkkkkkkkkkajjahh')
        serializer=userDataSerializer(userData,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message':'error','error':serializer.errors})
    
    def delete(self,request,pk,format=None):
        userData = self.get_object(pk)
        userData.delete()
        return Response({'message':'user deleted'})
# class setPagination(PageNumberPagination):
#     page_size=30
    
class userList(ListAPIView):
    queryset =CustomUser.objects.all()    
    serializer_class =userDataSerializer 
    # pagination_class= setPagination
    filter_backends =(SearchFilter,)
    search_fields =('username','email','first_name','last_name','profile_image')
    
class MyTokenObtainPairView(TokenObtainPairView): 
    serializer_class = myTokenObtainPairSerializer  
        
        
         
        