from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

class UserAuthentication(ObtainAuthToken):
    #authentication_classes = (TokenAuthentication)
    #permission_classes = ([AllowAny,SessionAuthentication, BasicAuthentication])
    #authentication_classes = ([IsAuthenticated])
    #http_method_names = ['get', 'head']

    #def get(self, request):
    #    model =Person.objects.all()
    #    serializer = UsersSerializer(model, many=True)
    #    return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get(user=user).key
        return Response(token)
        #print(token.key)

    #def get(self, request, format=None):
    #    content = {
    #        'user':str(request.user),
    #        'auth':str(request.auth)
    #    }
    #    return Response(content)

    #def get(self, request):
    #    model =Person.objects.all()
    #    serializer = UsersSerializer(model, many=True)
    #    return Response(serializer.data)

class UserList(APIView):

    permission_classes = ([AllowAny,])
    #authentication_classes = ([])

    def get(self, request):
        model =Person.objects.all()
        serializer = UsersSerializer(model, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    def get_user(self, Person):
        try:
            model = Users.objects.get(id=Person)
            return model
        except Users.DoesNotExist:
            return
        
    def get(self, request, Person):
        if not self.get_user(Person):
            return Response(f'User with {Person} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = UsersSerializer(self.get_user(Person))
        return Response(serializer.data)
        
    def put(self, request, Person):
        if not self.get_user(Person):
            return Response(f'User with {Person} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = UsersSerializer(self.get_user(Person), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, Person):
        if not self.get_user(Person):
            return Response(f'User with {Person} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        model = self.get_user(Person)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)