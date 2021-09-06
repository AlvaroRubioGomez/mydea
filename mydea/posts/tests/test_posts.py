"""Post unit tests"""

# Pytest
import pytest

# Mixer
from mixer.backend.django import mixer

# Graphene
from graphene.test import Client

# Graphql-jwt
from graphql_jwt.testcases import JSONWebTokenTestCase

# Utils
from mydea.utils.datetime import datetime_str_to_int

# Models
from mydea.users.models import User, Profile
from mydea.posts.models import Post

# Queries & Mutations
from .qm_variables_posts import (  
  my_posts_query,
  user_posts_query,
  all_posts,
  create_post_mutation,  
  edit_visibility_mutation,
  delete_post_mutation,  
)

@pytest.mark.django_db
class TestPost(JSONWebTokenTestCase): 
    """Post test case"""

    def setUp(self):  
        # Authenticated user           
        profile = mixer.blend(Profile)
        self.auth_user = profile.user                   
        self.client.authenticate(self.auth_user)       

        # Post data
        self.wrong_visibility = "PR"
        self.change_visibility = "PV"
        self.post_data = {            
            "visibility": "PT", # protected
            "body": "This is a dummy text"
        }

        # Posts
        self.posts_amount = 3
        for _ in range(self.posts_amount):
            mixer.blend(Post)
        
        # Authenticated user posts 
        self.auth_posts_amount = 5  
        self.auth_posts = [            
            self.client.execute(
                create_post_mutation,
                variables={
                    "body": "{} {}".format(self.post_data["body"], i),
                    "visibility": self.post_data["visibility"]
            }).data["createPost"]["post"]
            for i in range(self.auth_posts_amount)  
        ] 
        self.auth_posts.reverse() # descending created order        
        

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
        created_by = post["createdBy"]["user"]        

        self.assertTrue(success)
        self.assertIsNone(errors)    
        self.assertEqual(post["body"], self.post_data["body"])        
        self.assertEqual(post["visibility"], self.post_data["visibility"]) 
        self.assertEqual(created_by["username"], self.auth_user.username) 

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
        response = self.client.execute(
            create_post_mutation,
            variables={
                "body": self.post_data["body"],
                "visibility": self.wrong_visibility
        })        
        create_post = response.data["createPost"]
        success = create_post["success"]
        error = create_post["errors"][0]        

        self.assertFalse(success)   
        self.assertEqual(error["fieldName"], "visibility")
        self.assertEqual(
            error["messages"][0], 
            "Value '{}' is not a valid choice.".format(self.wrong_visibility)
        )

    
    def test_my_posts_query(self):
        """Unit test for retrieving all the posts of the
        authenticated user"""

        # Init
        created_by_arr = [] 
        created_arr = []

        response = self.client.execute(my_posts_query)
        post_collection = response.data["myPosts"]["edges"]        

        for i, post in enumerate(post_collection):
            # Get authenticated post data 
            auth_body = self.auth_posts[i]["body"]            
            
            # Get response post data
            res_body = post["node"]["body"]
            res_created = post["node"]["created"]
            res_created_by = post["node"]["createdBy"]

            # Get all posts created by username and created values
            created_by_arr.append(res_created_by["user"]["username"])
            created_arr.append(datetime_str_to_int(res_created))            
            
            # Check auth posts and response posts match
            self.assertEqual(auth_body, res_body)              
        
        # Check only auth user posts
        self.assertEqual(
            created_by_arr.count(self.auth_user.username),            
            self.auth_posts_amount)

        # Check descending order created (most recent first)
        prev_created = float('inf')
        for created in created_arr:            
            self.assertTrue(prev_created > created)
            prev_created = created

    
    def test_edit_visibility_query(self):
        """Unit test for editing a post visibility"""

        auth_post_id = self.auth_posts[0]["id"]

        response = self.client.execute(
            edit_visibility_mutation,
            variables={
                "id": auth_post_id,
                "visibility": self.change_visibility #PT -> PV
        })
        success = response.data["editVisibility"]["success"]
        errors = response.data["editVisibility"]["errors"]
        post = response.data["editVisibility"]["post"]

        self.assertTrue(success)
        self.assertIsNone(errors)
        self.assertEqual(post["id"], auth_post_id)
        self.assertEqual(post["visibility"], self.change_visibility)

    
    def test_delete_post(self):
        """Unit test for deleting a post"""

        auth_post_id = self.auth_posts[0]["id"]

        response = self.client.execute(
            delete_post_mutation,
            variables={"id": auth_post_id}
        )
        success = response.data["deletePost"]["success"]
        errors = response.data["deletePost"]["errors"]

        # Get remaining posts after delete
        response = self.client.execute(my_posts_query)
        post_collection = response.data["myPosts"]["edges"]

        self.assertTrue(success)
        self.assertIsNone(errors)
        self.assertEqual(
            len(post_collection), 
            self.auth_posts_amount - 1
        ) 
