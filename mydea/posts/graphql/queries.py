"""Post graphql queries"""

# Graphene
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay

# Django-graphql-auth
from graphql_jwt.decorators import login_required

# Types
from .types import PostNode 

# Models
from mydea.posts.models import Post
from mydea.users.models import Profile


class PostsQuery(graphene.ObjectType): 
    # post = relay.Node.Field(PostNode)      
    my_posts = DjangoFilterConnectionField(PostNode)    
    
    @login_required    
    def resolve_my_posts(root, info):       
        profile = info.context.user.profile      
        my_posts = Post.objects.filter(created_by=profile).all()
        
        return my_posts

    



