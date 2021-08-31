"""User unit tests"""

# Django
from django.test import TestCase
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
from mydea.users.models.users import User

# # Schema
# from config.schema import schema

# Queries & Mutations
from .users_qm_variables import (
  users_query,
  user_query,
  me_query,
  register_mutation,
  login_mutation
)


@pytest.mark.django_db
class TestUserAuth(JSONWebTokenTestCase): 
    """User test case"""

    def setUp(self):        
        # Create two anonymous users
        mixer.blend(User)
        mixer.blend(User)
        # Create an authenticated user        
        self.user = get_user_model().objects.create(
            username="test_username",
            first_name="test_name"
        )
        self.client.authenticate(self.user)

        # Override self.user.id with Node ID
        response = self.client.execute(
            users_query,
            variable_values={"first": 1}
        )                
        users = response.data["users"]["edges"]
        first_user = users[0]["node"]        
        self.user.id = first_user["id"]


    def test_users_query(self):
        """Unit test for retrieving all users"""

        response = self.client.execute(users_query)        
        users = response.data["users"]["edges"]
        first_user = users[0]["node"] 

        self.assertEqual(len(users), 3)
        self.assertEqual(first_user["id"], self.user.id)
        self.assertEqual(first_user["username"], self.user.username)


    def test_user_query(self):
        """Unit test for retrieving a single user"""

        response = self.client.execute(
            user_query,
            variables={"id": self.user.id}
        )        
        user = response.data["user"]     

        self.assertEqual(user["id"], self.user.id)
        self.assertEqual(user["username"], self.user.username)
        self.assertEqual(user["firstName"], self.user.first_name)   


    def test_me_query(self):
        response = self.client.execute(me_query)       
        user_me = response.data["me"]

        self.assertEqual(user_me["id"], self.user.id)
        self.assertEqual(user_me["username"], self.user.username)
        self.assertEqual(user_me["firstName"], self.user.first_name) 
        self.assertIsNotNone(user_me["created"])


    def test_register_mutation(self):
        """Unit test for registering an user"""

        # Dummy user data
        user_data = {
            "email": "dummyemail@gmail.com",
            "username": "dummy",
            "firstName": "Dummy Name",
            "lastName": "Dummy Lastname",            
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

    
    def test_login_mutation_successful(self):
        """Unit test for successful user login"""

        # Register dummy user
        user_data = {
            "email": "dummyemail@gmail.com",
            "username": "dummy",                        
            "password1": "megapass1234",
            "password2": "megapass1234"
        }
        self.client.execute(
            register_mutation, 
            variables = {**user_data}
        ) 

        response = self.client.execute(
            login_mutation,
            variables={
                "username": user_data["username"],
                "password": user_data["password1"]
        })        
        login = response.data["login"]
        user = login["user"]        

        self.assertTrue(login["success"])
        self.assertIsNone(login["errors"])
        self.assertIsNotNone(login["refreshToken"])
        self.assertIsNotNone(login["token"])
        self.assertEqual(user["username"], user_data["username"])
        self.assertEqual(user["email"], user_data["email"])


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



    # def test_update_user_mutation(self):
    #         """Unit test for updating an user"""

    #         # Dummy user data
    #         user_data = {
    #             "username": "updatedUsername",
    #             "firstName": "updated name"
    #         }

    #         response = self.client.execute(
    #             update_user_mutation,
    #             variable_values = {
    #                 "id": self.user.id,
    #                 **user_data,
    #         })
    #         update_user = response.get("data").get("updateUser").get("user")
    #         errors = response.get("data").get("updateUser").get("errors")

    #         assert errors is None
    #         assert update_user["username"] == user_data["username"]
    #         assert update_user["firstName"] == user_data["firstName"]
    #         assert update_user["lastName"] == self.user.last_name
    #         assert update_user["email"] == self.user.email

