from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json
from member.api.serializer import UserSerializer


class MemberCreationTestCase(APITestCase):
    """Define tests for Member creation"""
    def test_register_valid_member(self):
        """
        Test we can create/register a new user object.
        """
        url = '/api/members/'
        data = {'username': 'test_create_user',
                'email': 'test_create_user@email.com',
                'password': 'ghtybn12',
                'password2': 'ghtybn12'
                }
        response = self.client.post(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test_create_user')

    def test_register_valid_no_email(self):
        """
        Test we can create a new user with no value for email
        Email is NOT REQUIRED for user creation
        """
        url = '/api/members/'
        data = {'username': 'test_create_user',
                'password': 'youknownothing',
                'password2': 'youknownothing'
                }
        response = self.client.post(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_register_invalid_passwords(self):
        """
        Test we cannot create a new user object with mis-matched passwords.

        Should return a message of the mismatched passwords
        """
        url = '/api/members/'
        data = {'username': 'test_create_user',
                'email': 'test_create_user@email.com',
                'password': 'youknownothing',
                'password2': 'youdoknownothing'
                }
        response = self.client.post(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['password'], 'passwords must match')
        self.assertEqual(User.objects.count(), 0)

    def test_register_invalid_no_password(self):
        """
        Test we cannot create a new user object with no value for field password2

        Password2 is REQUIRED
        Should return a message notifying of requirement.
        """
        url = '/api/members/'
        data = {'username': 'test_create_user',
                'email': 'test_create_user@email.com',
                'password': 'youknownothing',
                }
        response = self.client.post(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['password2'][0], 'This field is required.')
        self.assertEqual(User.objects.count(), 0)

    def test_register_invalid_no_password(self):
        """
        Test we cannot create a new user object with no value for passsword field.

        password field is required to register a new user.
        """
        url = '/api/members/'
        data = {'username': 'test_create_user',
                'email': 'test_create_user@email.com',
                'password2': 'youdoknownothing'
                }
        response = self.client.post(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # write another assertion for checking the exact message here
        self.assertEqual(response.json()['password'][0], 'This field is required.')
        self.assertEqual(User.objects.count(), 0)


class MemberRetrieveTestCase(APITestCase):
    """
    Test member retrievals
    TO DO: Authentication.
    """
    def setUp(self):
        """
        Setup by creating a superuser and a standard user
        """
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.create(username="mike",  password="mikepw")

    def test_retrieve_member_list(self):
        """
        member list view
        Test we can  retrieve list of existing users.
        """
        url = reverse('members-list')
        response = self.client.get(url)
        data = response.json()[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['username'], "john")
    
    def test_retrieve_member_detail(self):
        """
        member detail view
        Test we can retrieve a specifc user given an id
        """
        url = '/api/members/2/'
        response = self.client.get(url, follow=True)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['username'], "mike")


class MemberUpdateTestCase(APITestCase):
    """
    Test Update on member models and it's viewsets
    TO DO: User authentication + Permission (ownership of the user account)
    
    """
    def setUp(self):
        """
        Setup by creating a superuser and a standard user
        """
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.create(username="mike",  password="mikepw")

    def test_put_username(self):
        """
        Test non-partial PUT method 

        TO DO:
        """
        url = '/api/members/2/'
        updated_name = 'mike-username-PUT'
        data = {'username': updated_name,
                'password': 'mikepw',
                'password2': 'mikepw'
                }
        response = self.client.put(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["username"], updated_name)
        self.assertEqual(User.objects.count(), 2)

    def test_put_username_missing_data(self):
        """
        Test partial PUT method with password missing
        Current setup, django default, doesn't allow partial PUT 
        """
        url = '/api/members/2/'
        updated_name = 'mike-username-PUT'
        data = {'username': updated_name,
                'password2': 'mikepw',
                }
        response = self.client.put(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['password'][0], 'This field is required.')

    
    def test_patch_username(self):
        """
        Test PATCH method for a user
        
        TO DO: Only authenticated user can path
               User can only path their own information not others 
        """
        url = '/api/members/2/'
        updated_name = 'mikePatched'
        data = {'username': updated_name,
                }
        response = self.client.patch(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["username"], updated_name)
        self.assertEqual(User.objects.count(), 2)


class MemberDeleteTestCase(APITestCase):
    """
    Test cases for member DELETE
    TO DO : User authentication + permission for deletion of self user
    """
    def setUp(self):
        """
        Setup by creating a superuser and a standard user
        """
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.create(username="mike",  password="mikepw")

    def test_delete_member(self):
        """
        Test deletion of a use rmember

        TO DO: Authenticate user is trying to delete itself not other user and is authenticated.
        """
        url = '/api/members/2/'
        response = self.client.delete(url, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)
