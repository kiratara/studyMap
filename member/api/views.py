from member.api.serializer import UserSerializer

from django.contrib.auth.models import User
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response


class MemberViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class =  UserSerializer


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


