from functools import wraps

# Graphene
from graphql_relay import from_global_id
from graphql import GraphQLError

# Utils
from mydea.utils.decorators import context

# Models
from mydea.posts.models import Post

def is_post_owner(f):
    @wraps(f)
    @context(f)
    def wrapper(context, *args, **kwargs): 
        # Get current post
        id = kwargs['id']
        post = Post.objects.get(pk=from_global_id(id)[1])
        # Check ownership
        if context.user != post.created_by:
            raise GraphQLError('You do not have permission to perform this action.')            
        return f(*args, **kwargs)
    return wrapper