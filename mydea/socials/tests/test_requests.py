"""Request unit tests"""

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
from mydea.socials.models import Request, Connection
from mydea.users.models import Profile, User

# Queries & Mutations
from .qm_variables_requests import (
    my_requests_query,
    resolve_request_mutation,
    send_request_mutation,
)


@pytest.mark.django_db
class TestRequest(JSONWebTokenTestCase): 
    """Request test case"""

    def setUp(self):  
        # Sender user        
        self.sender_connection = mixer.blend(Connection)
        self.sender_user = self.sender_connection.user
        # Receiver        
        self.receiver_connection = mixer.blend(Connection)
        self.receiver_user = self.receiver_connection.user

        # Request from 1st to 2nd
        self.request = Request.objects.create(
            sender = self.sender_user,
            receiver = self.receiver_user
        ) 
        # Rejectedted request
        Request.objects.create(
            sender = mixer.blend(User),
            receiver = self.receiver_user,
            status = 'R'
        ) 

    def test_my_requests_query(self):
        """Unit test for getting the sent requests to a 
        authenticated user."""       

        # Second user (receiver)
        self.client.authenticate(self.receiver_user)

        response = self.client.execute(my_requests_query)
        request_arr = response.data["myRequests"]["edges"]
        request = request_arr[0]["node"]
        sender = request["sender"]
        receiver = request["receiver"]
        status = request["status"]

        # Only request with sent status are retrieved
        self.assertEqual(len(request_arr), 1)                   
        self.assertEqual(sender["username"], self.sender_user.username)
        self.assertEqual(receiver["username"], self.receiver_user.username)
        self.assertEqual(status, 'S') 

    def test_resolve_request_mutation(self):
        """Unit test for resolving(accept/reject) a request
        by the receiver of this one"""       

        # Second user (receiver)
        self.client.authenticate(self.receiver_user)

        # Accept request
        response = self.client.execute(
            resolve_request_mutation,
            variables={
                "request_id": to_global_id('Request', self.request.id),
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
            self.receiver_user in list(self.sender_connection.following.all())
        )
        # Check sender added to receiver followers list
        self.assertTrue(
            self.sender_user in list(self.receiver_connection.followers.all())
        )

        # Reject request
        response = self.client.execute(
            resolve_request_mutation,
            variables={
                "request_id": to_global_id('Request', self.request.id),
                "action": "reject"
        })
        success = response.data["resolveRequest"]["success"]
        errors = response.data["resolveRequest"]["errors"]
        status = response.data["resolveRequest"]["request"]["status"]        
                             
        self.assertTrue(success)
        self.assertIsNone(errors)
        self.assertEqual(status, 'R') # accepted

    def test_send_request_mutation(self):
        """Unit test for sending a follow request
        to a authenticated user. By default, the
        request status should be 'S' (sent)"""      

        # first user (sender)
        self.client.authenticate(self.sender_user)

        response = self.client.execute(
            send_request_mutation,
            variables={
                "to_user_id": to_global_id(
                    'User', 
                    self.receiver_user.id
        )})       
        success = response.data["sendRequest"]["success"]
        errors = response.data["sendRequest"]["errors"]
        request = response.data["sendRequest"]["request"]
        sender = request["sender"]              
        receiver = request["receiver"]              
        status = request["status"]              

        self.assertTrue(success)
        self.assertIsNone(errors)    
        self.assertEqual(
            sender["username"], 
            self.sender_user.username
        )   
        self.assertEqual(
            receiver["username"], 
            self.receiver_user.username
        )  
        self.assertEqual(status, 'S')        