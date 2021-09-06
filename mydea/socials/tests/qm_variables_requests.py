"""Request queries and mutations variables"""

# Queries

my_requests_query = """
query{
  myRequests{
    edges{
      node{
        id,
        sender{
          username
        },
        receiver{
          username
        },
        status
      }
    }
  }
}
"""

# Mutations

resolve_request_mutation = """
mutation(
  $request_id:ID!,
	$action: Action!
){
  resolveRequest(
    input:{
      requestId:$request_id,
      action: $action
    }){
    success,
    errors{
      fieldName,
      messages
    },
    request{
      status
    }
  }
}
"""

send_request_mutation = """
mutation($to_user_id:ID!){
  sendRequest(
    input: {toUserId: $to_user_id}
  ){
    success,
    errors{
      fieldName,
      messages
    }
    request{
      sender{
        username
      },
      receiver{
        username
      },
      status
    }    
	}
}
"""