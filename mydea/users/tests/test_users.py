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
all_users_query = """
    query($index:Int){
        allUsers(first:$index){
            edges {
                node {
                    id,
                    username
                }
            }
        }
    }
"""


user_query = """
    query($id:ID!) {
        user(id: $id) {
            id,
            username,
            firstName
        }
    }
"""

# Mutations
create_user_mutation = """
    mutation(
        $username: String!,
        $firstName: String!,
        $lastName: String!,
        $email: String!,
        $password: String!
    ){
        createUser(input:{
            userData:{
                username: $username,
                firstName: $firstName,
                lastName: $lastName,
                email: $email,
                password: $password
            }
        }){
            user{
                id,
                username,
                firstName,
                lastName,
                email
            }
            errors{
                fieldName,
                messages
            }
        }
    }
"""

update_user_mutation = """
    mutation(
        $id:ID!,
        $username: String,
        $firstName: String
    ){
        updateUser(input:{
            id: $id,
            userData:{
                username: $username,
                firstName: $firstName
            }
        }){
            user{
                id,
                username,
                firstName,
                lastName,
                email
            }
            errors{
                fieldName,
                messages
            }
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
            all_users_query,
            variable_values={"index": 1}
        )
        users = response.get("data").get("allUsers").get("edges")
        self.user.id = users[0]["node"]["id"]


    def test_all_users_query(self):
        """Unit test for retrieving all users"""

        response = self.client.execute(all_users_query)
        users = response.get("data").get("allUsers").get("edges")

        assert len(users) == 3

    def test_user_query(self):
        """Unit test for retrieving a single user"""

        response = self.client.execute(
            user_query,
            variable_values={"id": self.user.id}
        )
        user = response.get("data").get("user")

        assert user["id"] == self.user.id
        assert user["username"] == self.user.username
        assert user["firstName"] == self.user.first_name

    def test_create_user_mutation(self):
        """Unit test for creating an user"""

        # Dummy user data
        user_data = {
            "username": "dummy",
            "firstName": "dummy name",
            "lastName": "dummy lastname",
            "email": "dummyemail@gmail.com",
            "password": "dummy password"
        }

        response = self.client.execute(create_user_mutation, variable_values = {**user_data})
        create_user = response.get("data").get("createUser").get("user")
        errors = response.get("data").get("createUser").get("errors")

        assert errors is None
        assert create_user["id"] is not None
        assert create_user["username"] == user_data["username"]
        assert create_user["firstName"] == user_data["firstName"]
        assert create_user["lastName"] == user_data["lastName"]
        assert create_user["email"] == user_data["email"]

    def test_duplicate_create_user_mutation(self):
        """Unit test for creating an existing username and email. It should return errors"""

        response = self.client.execute(
            create_user_mutation,
            variable_values = {
                "username": self.user.username,
                "firstName": self.user.first_name,
                "lastName": self.user.last_name,
                "email": self.user.email,
                "password": self.user.password
        })
        create_user = response.get("data").get("createUser").get("user")
        errors = response.get("data").get("createUser").get("errors")

        assert create_user is None
        assert errors[0]["fieldName"] == "username"
        assert errors[0]["messages"][0] == "A user with that username already exists."
        assert errors[1]["fieldName"] == "email"
        assert errors[1]["messages"][0] == "A user with that email already exists."

    def test_update_user_mutation(self):
        """Unit test for updating an user"""

        # Dummy user data
        user_data = {
            "username": "updatedUsername",
            "firstName": "updated name"
        }

        response = self.client.execute(
            update_user_mutation,
            variable_values = {
                "id": self.user.id,
                **user_data,
        })
        update_user = response.get("data").get("updateUser").get("user")
        errors = response.get("data").get("updateUser").get("errors")

        assert errors is None
        assert update_user["username"] == user_data["username"]
        assert update_user["firstName"] == user_data["firstName"]
        assert update_user["lastName"] == self.user.last_name
        assert update_user["email"] == self.user.email














