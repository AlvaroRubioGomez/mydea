"""Post unit tests"""

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
from mydea.posts.models.posts import Post

# Queries & Mutations
from .posts_qm_variables import (
  create_post_mutation,
)

@pytest.mark.django_db
class TestPost(JSONWebTokenTestCase): 
    """Post test case"""

    def setUp(self):  
        # Authenticated user        
        self.user = mixer.blend(User)          
        self.client.authenticate(self.user)

        # Post data
        self.post_data = {
            "wrong_visibility": "PR",
            "visibility": "PT", # protected
            "body": "This is a dummy text"
        }

    def test_create_post_mutation(self):
        """Unit test for creating a post.
        It should create a post with the given visibility and
        body and assigned autmatically the authenticated user 
        who created it"""      

        response = self.client.execute(
            create_post_mutation,
            variables={
                "body": self.post_data["body"],
                "visibility": self.post_data["visibility"]
        })        
        create_post = response.data["createPost"]
        success = create_post["success"]
        errors = create_post["errors"]
        post = create_post["post"]
        created_by = post["createdBy"]

        self.assertTrue(success)
        self.assertIsNone(errors)    
        self.assertEqual(post["body"], self.post_data["body"])        
        self.assertEqual(post["visibility"], self.post_data["visibility"]) 
        self.assertEqual(created_by["username"], self.user.username) 

    def test_create_post_mutation_visibility(self):
        """Unit test for the correct set up of the visibility property
        when creating a post.
            + Visibility should be PB (public) when not specified
            + An error should be arise when given a wrong visibility value"""

        # test default visibility
        response = self.client.execute(
            create_post_mutation,
            variables={"body": self.post_data["body"]}
        )        
        create_post = response.data["createPost"]
        success = create_post["success"]
        visibility = create_post["post"]["visibility"]

        self.assertTrue(success)               
        self.assertEqual(visibility, "PB")

        # test wrong visibility 
        wrong_visibility = self.post_data["wrong_visibility"]       
        response = self.client.execute(
            create_post_mutation,
            variables={
                "body": self.post_data["body"],
                "visibility": wrong_visibility
        })        
        create_post = response.data["createPost"]
        success = create_post["success"]
        error = create_post["errors"][0]        

        self.assertFalse(success)   
        self.assertEqual(error["fieldName"], "visibility")
        self.assertEqual(
            error["messages"][0], 
            "Value '{}' is not a valid choice.".format(wrong_visibility)
        )

    

                  
