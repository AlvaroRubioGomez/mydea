"""Connections queries and mutations variables"""

# Queries
my_following_query = """
query{
  myFollowing{
    edges{
      node{
        username,
        firstName       
      }
    }
  }
}
"""

my_followers_query = """
query{
  myFollowers{
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

delete_followers_mutation = """
mutation($user_id:ID!){
  deleteFollowers(
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