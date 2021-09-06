"""Post graphql queries"""

# Django
from django.db.models import Q

# Graphene
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from graphql_relay import from_global_id

# Django-graphql-auth
from graphql_jwt.decorators import login_required

# Types
from .types import PostNode 

# Models
from mydea.posts.models import Post
from mydea.users.models import User, Profile


class PostsQuery(graphene.ObjectType):         
    my_posts = DjangoFilterConnectionField(PostNode)
    user_posts = DjangoFilterConnectionField(
        PostNode,
        u_id = graphene.ID(required=True)
    )  
    
    @login_required    
    def resolve_my_posts(root, info): 
        # Get current user      
        profile = info.context.user.profile 
        # Get user posts     
        my_posts = Post.objects.filter(created_by=profile).all()        
        return my_posts

    @login_required    
    def resolve_user_posts(root, info, u_id):
        # Get current user
        request_user = info.context.user        
        # Get user by id
        user = User.objects.get(pk=from_global_id(u_id)[1])
        # Get user followers
        followers = user.profile.followers        
        # Get user posts
        if(user == request_user):
            user_posts = Post.objects.filter(created_by=user.profile)
        elif(followers.filter(id=request_user.id).exists()): # request user is a follower
            user_posts = Post.objects.filter(
                Q(created_by=user.profile) &
                Q(visibility='PB') | Q(visibility='PT')
            )
        else:
            user_posts = Post.objects.filter(
                created_by=user.profile,
                visibility='PB'
            )

        return user_posts   



