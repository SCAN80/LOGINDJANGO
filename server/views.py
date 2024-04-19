from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

@api_view(['POST'])
def login(request):
    print(request.data)
    user = User.objects.filter(username=request.data.get('username')).first()

    if not user or not user.check_password(request.data.get('password')):
        return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(serializer.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    print(request.user.id)
    serializer = UserSerializer(instance=request.user)
   
    return Response(serializer.data, status=status.HTTP_200_OK)
