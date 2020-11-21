from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serialize default Model user
    Used to user registration
    """   
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        """"""
        model = User
        fields = ["id", "username", "email", "password", "password2"]
        # set password to be write_only and have password style so the users see dot or * instead of text
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }
    
    def create(self, validated_data):
        """
        Currently, we are overriding the default super method save() which either calls update or create with the logic below.
        always create

        Save Profile instance with data after serializer has validated it
        Only save if password and password2 are a match.
        """
        self.password_match_check(validated_data) # if it's not a match, the error shouldve been raised and program 

        # email is not a REQUIRED field 
        if 'email' not in validated_data:
            email = None
        else:
            email = validated_data['email']
        user = User.objects.create_user(
                    email=email, 
                    username=self.validated_data['username'],
                    password=self.validated_data['password']
                )       
        return user

    def update(self, instance, validated_data):
        """
        Method called when User instance is updated
        called by the serializer classes save() method because the isntance already exists
        """
        if 'password' in validated_data and "password2" in validated_data: # PATCH 
            self.password_match_check(validated_data) # if it's not a match, the error shouldve been raised and program 
            instance.set_password(validated_data['password'])
        print (f"\n\n Message from the UserSerializer update method\n\n")
        return super().update(instance, validated_data)

    def password_match_check(self, validated_data):
        """ Confirm both passwords were provided and that they match"""
        password = validated_data['password']
        password2 = validated_data['password2'] # since the data is validated, there should always be both password

        if password != password2:
            raise serializers.ValidationError({'password': 'passwords must match'})
        return True
