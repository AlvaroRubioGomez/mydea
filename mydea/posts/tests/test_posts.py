"""Post unit tests"""

# Pytest
import pytest

# Mixer
from mixer.backend.django import mixer

# Graphene
from graphene.test import Client
from graphql_relay import to_global_id

# Graphql-jwt
from graphql_jwt.testcases import JSONWebTokenTestCase

# Utils
from mydea.utils.datetime import datetime_str_to_int

# Models
from mydea.users.models import User, Profile
from mydea.posts.models import Post
from mydea.socials.models import Connection

# Queries & Mutations
from .qm_variables_posts import (  
  my_posts_query,
  user_posts_query,
  all_posts_query,
  create_post_mutation,  
  edit_visibility_mutation,
  delete_post_mutation,  
)

@pytest.mark.django_db
class TestPost(JSONWebTokenTestCase): 
    """Post test case"""

    def setUp(self):        
        # Authenticated users  
        self.auth_users = []
        self.users_amount = 2
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
        
        # Posts
        # Post data
        self.posts = []
        self.wrong_visibility = "PR"
        self.change_visibility = "PV"
        self.visibility_arr = ["PB", "PV", "PT"]
        self.post_body = "dummy text"  

        # Create triplet of posts
        #   1 public, 1 private and 1 protected 
        #   for each auth user
        for user in self.auth_users:
            self.client.authenticate(user)
            user_posts = [
                self.client.execute(
                    create_post_mutation,
                    variables={
                        "body": "{}: {}-{}".format(
                            user.username,
                            self.post_body, 
                            visibility),
                        "visibility": visibility
                }).data["createPost"]["post"]
                for visibility in self.visibility_arr 
            ]
            user_posts.reverse() # descending created order 
            self.posts.append(user_posts)  

    
    def test_my_posts_query(self):
        """Unit test for retrieving all the posts of the
        authenticated user"""

        # Init
        created_by_arr = [] 
        created_arr = []

        # First user
        user = self.auth_users[0]
        self.client.authenticate(user)

        response = self.client.execute(my_posts_query)
        post_collection = response.data["myPosts"]["edges"]        

        for i, post in enumerate(post_collection):
            # Get authenticated post data 
            user_body = self.posts[0][i]["body"]            
            
            # Get response post data
            res_body = post["node"]["body"]
            res_created = post["node"]["created"]
            res_created_by = post["node"]["createdBy"]

            # Get all posts created by username and created values
            created_by_arr.append(res_created_by["user"]["username"])
            created_arr.append(datetime_str_to_int(res_created))            
            
            # Check auth posts and response posts match
            self.assertEqual(user_body, res_body)              
        
        # Check only auth user posts
        self.assertEqual(
            created_by_arr.count(user.username),            
            len(self.posts[0]))

        # Check descending order created (most recent first)
        prev_created = float('inf')
        for created in created_arr:            
            self.assertTrue(prev_created > created)
            prev_created = created


    def test_user_posts_query_by_follower(self):
        """Unit test for retrieving all given user's posts.
        Execute by a follower it should return public and
        protected posts but not private ones"""        

        # Init
        created_by_arr = [] 
        created_arr = []

        # First user
        fst_user = self.auth_users[0]        

        # Second user
        snd_user = self.auth_users[1]

        self.client.authenticate(fst_user)        
        response = self.client.execute(
            user_posts_query,
            variables={
                "userId": to_global_id('User', snd_user.id)
        })           
        snd_user_posts = response.data["userPosts"]["edges"]      

        for i, post in enumerate(snd_user_posts):           
            # Get response post data            
            res_created = post["node"]["created"]
            res_created_by = post["node"]["createdBy"]
            res_visibility = post["node"]["visibility"]

            # Get all posts created by username and created values
            created_by_arr.append(res_created_by["user"]["username"])
            created_arr.append(datetime_str_to_int(res_created))           
           
            # Check post visibility is not private
            self.assertNotEqual(
                res_visibility, 
                self.visibility_arr[1] #PV
            ) 
        
        # Check only second user posts
        self.assertEqual(
            created_by_arr.count(snd_user.username),            
            len(snd_user_posts))

        # Check descending order created (most recent first)
        prev_created = float('inf')
        for created in created_arr:            
            self.assertTrue(prev_created > created)
            prev_created = created

    
    def test_user_posts_query_by_non_follower(self):
        """Unit test for retrieving all given user's posts.
        Execute by a non-follower it should return only
        public posts"""         

        # Init
        created_by_arr = [] 
        created_arr = []

        # Non follower user
        non_f_user = mixer.blend(User)        

        # Second user
        snd_user = self.auth_users[1]

        self.client.authenticate(non_f_user)
        response = self.client.execute(
            user_posts_query,
            variables={
                "userId": to_global_id('User', snd_user.id)
        })        
        snd_user_posts = response.data["userPosts"]["edges"]      

        for i, post in enumerate(snd_user_posts):           
            # Get response post data            
            res_created = post["node"]["created"]
            res_created_by = post["node"]["createdBy"]
            res_visibility = post["node"]["visibility"]

            # Get all posts created by username and created values
            created_by_arr.append(res_created_by["user"]["username"])
            created_arr.append(datetime_str_to_int(res_created))           
           
            # Check post visibility is public
            self.assertEqual(
                res_visibility, 
                self.visibility_arr[0] #PB
            ) 
        
        # Check only second user posts
        self.assertEqual(
            created_by_arr.count(snd_user.username),            
            len(snd_user_posts))

        # Check descending order created (most recent first)
        prev_created = float('inf')
        for created in created_arr:            
            self.assertTrue(prev_created > created)
            prev_created = created

    
    def test_all_posts_query(self):
        """Unit test for retrieving a timeline of
        all the authenticated user's posts and
        user's following's posts taking into account
        the post's visibility"""        

        # Init
        fst_user_posts = []
        snd_user_posts = []        
        created_arr = []

        # First user
        fst_user = self.auth_users[0]        

        # Second user
        snd_user = self.auth_users[1]

        self.client.authenticate(fst_user)
        response = self.client.execute(all_posts_query)               
        all_posts = response.data["allPosts"]["edges"]        

        for post in all_posts:
            # Get response post data            
            res_created = post["node"]["created"]
            res_created_by = post["node"]["createdBy"]                     
            username = res_created_by["user"]["username"]
            
            # Get all posts created values            
            created_arr.append(datetime_str_to_int(res_created)) 
            
            # First user's post (request user)
            if(username == fst_user.username):
                fst_user_posts.append(post)

            # Second user's post
            if(username == snd_user.username):
                snd_user_posts.append(post)

        # Check descending order created (most recent first)
        prev_created = float('inf')
        for created in created_arr:            
            self.assertTrue(prev_created > created)
            prev_created = created

        # Check all post from first user
        self.assertEqual(
            len(fst_user_posts),
            len(self.posts[0])
        )

        # Check number and visibility from second user's posts
        self.assertEqual(
            len(snd_user_posts),
            len(self.visibility_arr)-1
        )
        self.assertNotEqual(
            (p["visibility"] for p in snd_user_posts),
            self.visibility_arr[1] #PV
        )       
        

    def test_create_post_mutation(self):
        """Unit test for creating a post.
        It should create a post with the given visibility and
        body and assigned autmatically the authenticated user 
        who created it"""      

        # First user
        user = self.auth_users[0]
        self.client.authenticate(user)

        response = self.client.execute(
            create_post_mutation,
            variables={
                "body": self.post_body,
                "visibility": self.visibility_arr[-1] #PT
        })            
        create_post = response.data["createPost"]
        success = create_post["success"]
        errors = create_post["errors"]
        post = create_post["post"]
        created_by = post["createdBy"]["user"]        

        self.assertTrue(success)
        self.assertIsNone(errors)    
        self.assertEqual(post["body"], self.post_body)        
        self.assertEqual(post["visibility"], self.visibility_arr[-1]) 
        self.assertEqual(created_by["username"], user.username) 

    def test_create_post_mutation_visibility(self):
        """Unit test for the correct set up of the visibility property
        when creating a post.
            + Visibility should be PB (public) when not specified
            + An error should be arise when given a wrong visibility value"""

        # First user
        user = self.auth_users[0]
        self.client.authenticate(user)

        # test default visibility
        response = self.client.execute(
            create_post_mutation,
            variables={"body": self.post_body}
        )        
        create_post = response.data["createPost"]
        success = create_post["success"]
        visibility = create_post["post"]["visibility"]

        self.assertTrue(success)               
        self.assertEqual(visibility, self.visibility_arr[0]) #PB

        # test wrong visibility                
        response = self.client.execute(
            create_post_mutation,
            variables={
                "body": self.post_body,
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

    
    def test_edit_visibility_query(self):
        """Unit test for editing a post visibility"""

        # First user
        user = self.auth_users[0]
        self.client.authenticate(user)

        # First post 
        user_post = self.posts[0][0]       

        # Check visibility pre-edit        
        self.assertEqual(
            user_post["visibility"],
            self.visibility_arr[-1] #PT
        )

        response = self.client.execute(
            edit_visibility_mutation,
            variables={
                "id": user_post["id"],
                "visibility": self.change_visibility #PT -> PV
        })
        success = response.data["editVisibility"]["success"]
        errors = response.data["editVisibility"]["errors"]
        res_post = response.data["editVisibility"]["post"]

        self.assertTrue(success)
        self.assertIsNone(errors)
        self.assertEqual(res_post["id"], user_post["id"])
        self.assertEqual(res_post["visibility"], self.change_visibility)
    

    def test_delete_post(self):
        """Unit test for deleting a post"""

        # First user
        user = self.auth_users[0]
        self.client.authenticate(user)

        # First post id        
        post_id = self.posts[0][0]["id"]

        response = self.client.execute(
            delete_post_mutation,
            variables={"id": post_id}
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
            len(self.posts[0])-1
        ) 
        

