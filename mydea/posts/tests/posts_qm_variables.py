"""Post queries and mutations variables"""


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