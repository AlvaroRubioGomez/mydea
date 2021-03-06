"""Connections unit tests"""

# Django
from django.contrib.auth import get_user_model

# Pytest
import pytest

# Mixer
from mixer.backend.django import mixer

# Graphene
from graphene.test import Client
from graphql_relay import to_global_id

# Graphql-jwt
from graphql_jwt.testcases import JSONWebTokenTestCase

# Models
from mydea.users.models import Profile, User
from mydea.socials.models import Connection

# Queries & Mutations
from .qm_variables_connections import (
  my_following_query, 
  my_followers_query, 
  delete_following_mutation,
  delete_followers_mutation,
)


@pytest.mark.django_db
class TestConnection(JSONWebTokenTestCase): 
    """Connection test case"""

    def setUp(self):  
        # Authenticated users  
        self.auth_users = []
        self.users_amount = 3
        for _ in range(self.users_amount):           
            user = mixer.blend(User)             
            profile = mixer.blend(Profile, user=user)
            connection = mixer.blend(Connection, user=user)
            self.auth_users.append(user)             
         
        # Follow and get followed by each other
        for i in range(self.users_amount):
            for j in range(self.users_amount-1):
                # Add following and followers the other users by traversing backwards
                self.auth_users[i].connection.following.add(self.auth_users[i-j-1])
                self.auth_users[i].connection.followers.add(self.auth_users[i-j-1])

        
    def test_my_following_query(self):
        """Unit test for getting the following of authenticated
        user."""       

        # First user
        first_auth_user = self.auth_users[0]        
        following_usernames = [ 
            first_auth_user.connection.following.all()[i].username
            for i in range(self.users_amount-1)
        ]   
        
        self.client.authenticate(first_auth_user)
        response = self.client.execute(my_following_query)
        res_following_arr = response.data["myFollowing"]["edges"] 
        
        # Check right amount of following users
        self.assertEqual(len(res_following_arr), self.users_amount-1)        
        # Check following users belongs to user's following list
        for following_user in res_following_arr:
            res_username = following_user["node"]["username"]                      
            self.assertTrue(res_username in following_usernames)

    def test_my_followers_query(self):
        """Unit test for getting the followers of authenticated
        user."""       

        # First user
        first_auth_user = self.auth_users[0]        
        followers_usernames = [ 
            first_auth_user.connection.followers.all()[i].username
            for i in range(self.users_amount-1)
        ]   
        
        self.client.authenticate(first_auth_user)
        response = self.client.execute(my_followers_query)
        res_followers_arr = response.data["myFollowers"]["edges"] 
        
        # Check right amount of followers users
        self.assertEqual(len(res_followers_arr), self.users_amount-1)        
        # Check followers users belongs to user's followers list
        for followers_user in res_followers_arr:
            res_username = followers_user["node"]["username"]                      
            self.assertTrue(res_username in followers_usernames)


    def test_delete_following_mutation(self):
        """Unit test for deleting following user of an 
        authenticated user"""       

        # First user
        first_auth_user = self.auth_users[0]
        # Second user 
        second_auth_user = self.auth_users[1] 
        
        self.client.authenticate(first_auth_user)        
        response = self.client.execute(
            delete_following_mutation,
            variables={
                "user_id": to_global_id('User', second_auth_user.id)
        })
        success = response.data["deleteFollowing"]["success"] 
        errors = response.data["deleteFollowing"]["errors"] 
             
        # Check success
        self.assertTrue(success) 
        self.assertIsNone(errors) 
        # Check remaining users
        remain_user_amount = len(first_auth_user.connection.following.all())        
        # Check second user no longer in first user following
        following_usernames = [ 
            first_auth_user.connection.following.all()[i].username
            for i in range(remain_user_amount)
        ]   
        self.assertTrue(
            second_auth_user.username not in following_usernames
        )
        # Check first user no longer in second user followers
        followers_usernames = [ 
            second_auth_user.connection.followers.all()[i].username
            for i in range(remain_user_amount)
        ]   
        self.assertTrue(
            first_auth_user.username not in followers_usernames
        )

    def test_delete_followers_mutation(self):
        """Unit test for deleting followers user of an 
        authenticated user"""       

        # First user
        first_auth_user = self.auth_users[0]
        # Second user 
        second_auth_user = self.auth_users[1] 
        
        self.client.authenticate(first_auth_user)        
        response = self.client.execute(
            delete_followers_mutation,
            variables={
                "user_id": to_global_id('User', second_auth_user.id)
        })
        success = response.data["deleteFollowers"]["success"] 
        errors = response.data["deleteFollowers"]["errors"] 
             
        # Check success
        self.assertTrue(success) 
        self.assertIsNone(errors) 
        # Check remaining users
        remain_user_amount = len(first_auth_user.connection.followers.all())        
        # Check second user no longer in first user followers
        followers_usernames = [ 
            first_auth_user.connection.followers.all()[i].username
            for i in range(remain_user_amount)
        ]   
        self.assertTrue(
            second_auth_user.username not in followers_usernames
        )
        # Check first user no longer in second user following
        following_usernames = [ 
            second_auth_user.connection.following.all()[i].username
            for i in range(remain_user_amount)
        ]   
        self.assertTrue(
            first_auth_user.username not in following_usernames
        )