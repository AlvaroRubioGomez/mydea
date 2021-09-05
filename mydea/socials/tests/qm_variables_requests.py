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
  $r_id:ID!,
	$action: Action!
){
  resolveRequest(
    input:{
      rId:$r_id,
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