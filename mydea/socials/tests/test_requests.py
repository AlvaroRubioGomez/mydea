"""Request unit tests"""

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
from mydea.socials.models import Request
from mydea.users.models import Profile

# Queries & Mutations
from .qm_variables_requests import (
    my_requests_query,
    resolve_request_mutation,
)


@pytest.mark.django_db
class TestRequest(JSONWebTokenTestCase): 
    """Request test case"""

    def setUp(self):  
        # Sender user
        self.sender_profile = mixer.blend(Profile)
        self.sender_user = self.sender_profile.user
        # Receiver
        self.receiver_profile = mixer.blend(Profile)
        self.receiver_user = self.receiver_profile.user

        # Request from 1st to 2nd
        self.request = Request.objects.create(
            sender = self.sender_user,
            receiver = self.receiver_user
        ) 

    def test_my_requests_query(self):
        """Unit test for getting the sent requests to a 
        authenticated user."""       

        # Second user (receiver)
        self.client.authenticate(self.receiver_user)

        response = self.client.execute(my_requests_query)
        request = response.data["myRequests"]["edges"][0]["node"]
        sender = request["sender"]
        receiver = request["receiver"]
        status = request["status"]
                             
        self.assertEqual(sender["username"], self.sender_user.username)
        self.assertEqual(receiver["username"], self.receiver_user.username)
        self.assertEqual(status, 'S') # sent by default

    def test_resolve_request_mutation(self):
        """Unit test for resolving(accept/reject) a request
        by the receiver of this one"""       

        # Second user (receiver)
        self.client.authenticate(self.receiver_user)

        # Accept request
        response = self.client.execute(
            resolve_request_mutation,
            variables={
                "r_id": to_global_id('Request', self.request.id),
                "action": "accept"
        })
        success = response.data["resolveRequest"]["success"]
        errors = response.data["resolveRequest"]["errors"]
        status = response.data["resolveRequest"]["request"]["status"]        
                             
        self.assertTrue(success)
        self.assertIsNone(errors)
        self.assertEqual(status, 'A') # accepted
        # Check receiver added to sender following list
        self.assertTrue(
            self.receiver_user in list(self.sender_profile.following.all())
        )
        # Check sender added to receiver followers list
        self.assertTrue(
            self.sender_user in list(self.receiver_profile.followers.all())
        )

        # Reject request
        response = self.client.execute(
            resolve_request_mutation,
            variables={
                "r_id": to_global_id('Request', self.request.id),
                "action": "reject"
        })
        success = response.data["resolveRequest"]["success"]
        errors = response.data["resolveRequest"]["errors"]
        status = response.data["resolveRequest"]["request"]["status"]        
                             
        self.assertTrue(success)
        self.assertIsNone(errors)
        self.assertEqual(status, 'R') # accepted