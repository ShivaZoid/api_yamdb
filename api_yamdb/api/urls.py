# from django.urls import include, path
# from rest_framework.routers import DefaultRouter

# from .views import *

# app_name = 'api'

# router_v1 = DefaultRouter()

# router_v1.register(
#     'titles',
#     ...,
#     basename='titles'
# )
# router_v1.register(
#     'categories',
#     ...,
#     basename='сategories'
# )
# router_v1.register(
#     'genres',
#     ...,
#     basename='genres'
# )
# router_v1.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ...,
#     basename='reviews'
# )
# router_v1.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     ...,
#     basename='comments'
# )

# urlpatterns = [
#     path('v1/', include(router_v1.urls)),
# ]