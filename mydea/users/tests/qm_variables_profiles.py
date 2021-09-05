"""Profile queries and mutations variables"""

# Queries
following_query = """
query{
  following{
    edges{
      node{
        username,
        firstName       
      }
    }
  }
}
"""

followers_query = """
query{
  followers{
    edges{
      node{
        username,
        firstName       
      }
    }
  }
}
"""

# Mutations

delete_following_mutation = """
mutation($user_id:ID!){
  deleteFollowing(
    input:{userId: $user_id}
  ){
    success, 
    errors{
      fieldName,
      messages
    }
  }
}
"""