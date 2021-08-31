"""Main URLs module."""

# Django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

# Graphene
from graphene_django.views import GraphQLView


urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),

    # Graphql
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True)))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

