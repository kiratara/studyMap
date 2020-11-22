from django.contrib.auth.models import User
from rest_framework import filters, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics

from member.api.serializer import UserSerializer


class MemberRegisterView(CreateAPIView):
    """Concrete view for creating member instances"""
    queryset = User.objects.all()
    serializer_class =  UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({'token': token.key, 'username': serializer.instance.username}, status=status.HTTP_201_CREATED)


class MemberLisAPIView(ListAPIView):
    """
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MemberRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            # 'email': user.email
        })


# class MemberViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class =  UserSerializer
#     # authentication_classes = [TokenAuthentication]

# class MemberRegisterView(CreateAPIView):
#     """Handle user login"""
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

    # def create(self, request, *args, **kwargs):
        # response = super().create(request, *args, **kwargs)
        # print (f"This is the response from creating a new user: {response.data}")
        # user = User.objects.get(email__exact=response.data['email'])
        # token, created = Token.objects.get_or_create(user=user)
        # print (f"This is supposed to be the token: {token}")
        # response['token'] = token.key
        # print ("This is the final response")
        # return Response(response, status=status.HTTP_201_CREATED)
