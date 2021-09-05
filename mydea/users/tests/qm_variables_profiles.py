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