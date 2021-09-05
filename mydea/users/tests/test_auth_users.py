"""User unit tests"""

# Django
from django.contrib.auth import get_user_model

# Pytest
import pytest

# Mixer
from mixer.backend.django import mixer

# Graphene
from graphene.test import Client

# Graphql-jwt
from graphql_jwt.testcases import JSONWebTokenTestCase

# Models
from mydea.users.models import User

# Queries & Mutations
from .qm_variables_users import (
  users_query,
  register_mutation,
  login_mutation,
  password_change_mutation
)


@pytest.mark.django_db
class TestUserAuth(JSONWebTokenTestCase): 
    """User test case"""

    def setUp(self):        
        # Anonymous users
        mixer.blend(User)
        mixer.blend(User)             

        # Registered user
        self.user_data = {
            "email": "dummyemail@gmail.com",
            "username": "dummy",                        
            "password1": "megapass1234",
            "password2": "megapass1234"
        }
        self.client.execute(register_mutation, variables = {**self.user_data})        
        self.registered_user = get_user_model().objects.get(
            username=self.user_data["username"]
        )
        self.client.authenticate(self.registered_user)                   


    def test_users_query(self):
        """Unit test for retrieving all users"""

        response = self.client.execute(users_query)        
        users = response.data["users"]["edges"]
        first_user = users[0]["node"] 

        self.assertEqual(len(users), 3)        
        self.assertEqual(first_user["username"], self.registered_user.username)


    def test_register_mutation(self):
        """Unit test for registering an user with automatic 
        account verification"""

        # Dummy user data
        user_data = {
            "email": "example@gmail.com",
            "username": "example",
            "firstName": "example name",
            "lastName": "example lastname",            
            "password1": "megapass1234",
            "password2": "megapass1234"
        }

        response = self.client.execute(
            register_mutation, 
            variables = {**user_data}
        )        
        register = response.data["register"]                
        
        self.assertTrue(register["success"])
        self.assertIsNone(register["errors"])
        self.assertIsNotNone(register["refreshToken"])
        self.assertIsNotNone(["token"])         
        # Check auto-verified user
        user = User.objects.get(pk=self.registered_user.id)
        self.assertTrue(user.status.verified)

    
    def test_login_mutation_successful(self):
        """Unit test for successful user login"""       

        response = self.client.execute(
            login_mutation,
            variables={
                "username": self.registered_user.username,
                "password": self.user_data["password1"]
        })        
        login = response.data["login"]
        user = login["user"]        

        self.assertTrue(login["success"])
        self.assertIsNone(login["errors"])
        self.assertIsNotNone(login["refreshToken"])
        self.assertIsNotNone(login["token"])
        self.assertEqual(user["username"], self.registered_user.username)
        self.assertEqual(user["email"], self.registered_user.email)


    def test_login_mutation_invalid_credentials(self):
        """Unit test for user login with invalid credentials"""
        
        # No previous user registration

        response = self.client.execute(
            login_mutation,
            variables={
                "username": "non_existing_user",
                "password": "non_existing_password"
        })        
        login = response.data["login"]
        user = login["user"] 
        errors = login["errors"] 

        self.assertIsNone(login["token"])
        self.assertIsNone(login["refreshToken"])        
        self.assertIsNone(user)        
        self.assertFalse(login["success"])       
        self.assertEqual(errors["nonFieldErrors"][0]["code"], "invalid_credentials") 


    def test_password_change_mutation(self):
        """Unit test for changing the password"""

        # new password
        new_pass = "newmegapass1234"

        response = self.client.execute(
            password_change_mutation,
            variables={
                "oldPassword": self.user_data["password1"],
                "newPassword1": new_pass,
                "newPassword2": new_pass
        })  

        pass_change = response.data["passwordChange"]          

        self.assertTrue(pass_change["success"])
        self.assertIsNotNone(pass_change["token"])
        self.assertIsNotNone(pass_change["refreshToken"])        
        self.assertIsNone(pass_change["errors"])        
         


