"""User unit tests"""

# Django
from django.test import TestCase

# Pytest
import pytest

# Mixer
from mixer.backend.django import mixer

# Graphene
from graphene.test import Client

# Models
from mydea.users.models.users import User

# Schema
from config.schema import schema

# Queries
users_query = """
query($first: Int){
  users(first: $first){
    edges{
      node{
        id,
        username
      }
    }
  }
}
"""

user_query = """
query($id: ID!){
  user(id: $id){
    id,
    username,
    firstName
  }
}
"""

# Mutations
register_mutation = """
mutation(
  $email: String!,
  $username: String!,
  $password1: String!,
  $password2: String!
	){
    register(
      email: $email,
      username: $username,
      password1: $password1,
      password2: $password2
    ){
      success,
      errors,
      refreshToken,
      token
    }
}
"""


@pytest.mark.django_db
class TestUserSchema(TestCase):
    """User test case"""

    def setUp(self):
        self.client = Client(schema)
        # Create three users
        mixer.blend(User)
        mixer.blend(User)
        self.user = mixer.blend(User)

        # Override self.user.id with Node ID
        response = self.client.execute(
            users_query,
            variable_values={"first": 1}
        )
        users = response.get("data").get("users").get("edges")
        first_user = users[0].get("node")
        self.user.id = first_user["id"]


    def test_users_query(self):
        """Unit test for retrieving all users"""

        response = self.client.execute(users_query)        
        users = response.get("data").get("users").get("edges")
        first_user = users[0].get("node")        

        assert len(users) == 3
        assert first_user["id"] == self.user.id
        assert first_user["username"] == self.user.username


    def test_user_query(self):
        """Unit test for retrieving a single user"""

        response = self.client.execute(
            user_query,
            variable_values={"id": self.user.id}
        )
        #import pdb; pdb.set_trace()
        user = response.get("data").get("user")        

        assert user["id"] == self.user.id
        assert user["username"] == self.user.username
        assert user["firstName"] == self.user.first_name    


    # def test_register_mutation(self):
    #     """Unit test for registering an user"""

    #     # Dummy user data
    #     user_data = {
    #         "email": "dummyemail@gmail.com",
    #         "username": "dummy",
    #         # "firstName": "dummy name",
    #         # "lastName": "dummy lastname",            
    #         "password1": "dummypass1234",
    #         "password2": "dummypass1234"
    #     }

    #     response = self.client.execute(
    #         register_mutation, 
    #         variable_values = {**user_data}
    #     )
    #     variable_values = {**user_data}
    #     import pdb; pdb.set_trace()
    #     register = response.get("data").get("register")        
        
    #     assert register["success"] is True
    #     assert register["errors"] is None
    #     assert register["refreshToken"] is not None
    #     assert register["token"] is not None            


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

