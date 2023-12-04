from importlib.resources import is_resource
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User=get_user_model()

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post (self, request):
        try:
            data=request.data
            name=data.get('name').lower()
            email=data.get('email')
            password=data.get('password')
            re_password=data.get('re_password')
            is_realtor=data.get('is_realtor')
                        
            if password != re_password:
                return Response({'error':'passwords do not match'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                if not User.objects.filter(email=email).exists():
                    if is_realtor=='False':
                        User.objects.create_user(email=email,name=name,password=password)
                        return Response({'success':'User created successfully'}, status=status.HTTP_201_CREATED)
                    else:
                        User.objects.create_realtor(email=email,name=name,password=password)
                        return Response({'success':'Realtor created successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error':'User with the email exists'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)                    
                  
        except Exception as e:
            print(e)
            return Response({'error':e},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
class RetrieveUserView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user=UserSerializer(request.user)
            return Response({'user':user.data},
                            status=status.HTTP_200_OK)
        except:
            return Response({'error':'Something went wrong when retrieving user'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)