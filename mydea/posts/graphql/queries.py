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
        user_id = graphene.ID(required=True)
    ) 
    all_posts = DjangoFilterConnectionField(PostNode)
    
    @login_required    
    def resolve_my_posts(root, info): 
        # Get current user's profile     
        profile = info.context.user.profile 
        # Get user's posts     
        my_posts = Post.objects.filter(created_by=profile).all()        
        return my_posts

    @login_required    
    def resolve_user_posts(root, info, user_id):
        # Get current user
        request_user = info.context.user        
        # Get user by id
        user = User.objects.get(pk=from_global_id(user_id)[1])
        # Get user's followers
        followers = user.connection.followers               
        # Get user posts
        if(user == request_user):
            user_posts = Post.objects.filter(created_by=user.profile).all()

        is_follower = followers.filter(id=request_user.id).exists() 
        if(is_follower): # request user is a follower
            user_posts = Post.objects.filter(
                Q(created_by=user.profile) &
                (Q(visibility='PB') | Q(visibility='PT'))
            ).all()
            #import pdb; pdb.set_trace() 
        else:
            user_posts = Post.objects.filter(
                created_by=user.profile,
                visibility='PB'
            ).all()

        return user_posts   

    @login_required    
    def resolve_all_posts(root, info):
        # Get current user
        user = info.context.user        
        # Get user's following
        following = user.connection.following             
        # Get user's and following user's posts
        all_posts = Post.objects.filter(
            # Get all publics posts
            Q(visibility='PB') 
            # Get all protected posts of user's following
            | Q(created_by__in=[user.profile for user in following.all()]) 
                & Q(visibility='PT') 
            # Get all user's privates and protected posts          
            | Q(created_by=user.profile) & 
            (Q(visibility='PV') | Q(visibility='PT'))          
        ).all()      

        return all_posts 



