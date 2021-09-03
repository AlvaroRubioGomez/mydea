"""Post queries and mutations variables"""

# Queries

my_posts_query = """
query{
	myPosts{
    edges{
      node{
        body,
        created,
        createdBy{
          username
        }
      }
    }
  }
}
"""

# Mutations

create_post_mutation = """
mutation(
  $visibility: String,
  $body: String!
	){
    createPost(
      input:{
        visibility: $visibility,
        body: $body
      }){
        success,
        post{
          id,
          created,
          visibility,
          body,
          createdBy{
            username
          }
        }
        errors{
          fieldName,
          messages
        }
    }
}
"""

edit_visibility_mutation = """
mutation(
  $id: ID!
  $visibility: String!
){
  editVisibility(
    input: {
      id: $id,
      visibility: $visibility
    }){
    success,
    post{
      id,
      visibility
    }
    errors{
      fieldName,
      messages
    }
    
  }
}
"""

