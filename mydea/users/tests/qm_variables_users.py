"""User queries and mutations variables"""

# Queries
find_users_query = """
query($first: Int, $username: String){
  findUsers(first: $first, username: $username){
    edges{
      node{
        id,
        username,
        firstName,
        lastName,
        email,
        created
      }
    }
  }
}
"""

# Mutations
register_mutation = """
mutation(
  $email: String!,
  $username: String!,
  $password1: String!,
  $password2: String!
	){
    register(
      email: $email,
      username: $username,
      password1: $password1,
      password2: $password2
    ){
      success,
      errors,
      refreshToken,
      token
    }
}
"""

login_mutation = """
mutation(
  $username: String!, 
  $password:String!
){
  login(
    username: $username, 
    password: $password
  ){
    success,
    errors,
    token,
    refreshToken,
    user{
      id,
      username,
      email
    }
  }
}
"""

password_change_mutation = """
mutation(
  $oldPassword: String!
	$newPassword1: String!
	$newPassword2: String!
){
  passwordChange(
    oldPassword: $oldPassword,
		newPassword1: $newPassword1,
		newPassword2: $newPassword2
  ){
    success,
    errors,
    refreshToken,
    token
  }   
}
"""