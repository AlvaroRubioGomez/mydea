"""Post decorators unit tests"""

# Pytest
import pytest

# Mixer
from mixer.backend.django import mixer

# Graphene
from graphene.test import Client

# Graphql-jwt
from graphql_jwt.testcases import JSONWebTokenTestCase

# Models
from mydea.users.models import User, Profile
from mydea.posts.models import Post

# Queries & Mutations
from .qm_variables_posts import (
  create_post_mutation, 
  delete_post_mutation,
)

@pytest.mark.django_db
class TestPostDecorators(JSONWebTokenTestCase): 
    """Post decorators test case"""

    def setUp(self):
        # Post data       
        self.post_data = {   
            "body": "This is a dummy text"
        }

        # Posts from diff users
        self.auth_posts = []
        for _ in range(2):
            # Authenticated user       
            profile = mixer.blend(Profile)
            self.auth_user = profile.user                   
            self.client.authenticate(self.auth_user)        

            # Posts
            self.auth_posts.append(
                self.client.execute(
                    create_post_mutation,
                    variables={
                        **self.post_data               
                }).data["createPost"]["post"]
            )

    def test_is_post_owner_decorator(self):
        """Unit test for is_post_owner decorator.
        It should return a non-permission error when
        a user try to delete a post which was not
        created by him.        
        On the other hand, it should allow deleting a 
        post by the user who created the post."""  

        first_post_id = self.auth_posts[0]["id"]
        second_post_id = self.auth_posts[1]["id"]
        # Notice the client is the second user

        # Check wrong permissions        
        response = self.client.execute(
            delete_post_mutation,
            variables={"id": first_post_id}
        )        
        delete_post = response.data["deletePost"]
        error_message = response.errors[0].message

        self.assertIsNone(delete_post)
        self.assertEqual(
            error_message, 
            'You do not have permission to perform this action.'
        )

        # Check right permissions
        response = self.client.execute(
            delete_post_mutation,
            variables={"id": second_post_id}
        )   
        success = response.data["deletePost"]["success"]
        errors = response.data["deletePost"]["errors"]        

        self.assertTrue(success)
        self.assertIsNone(errors)    