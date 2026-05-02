from django.urls import path  # type:ignore
from rest_framework_simplejwt.views import TokenObtainPairView  # type:ignore
from rest_framework_simplejwt.views import TokenRefreshView  # type:ignore
from rest_framework_simplejwt.views import TokenVerifyView  # type:ignore
from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet


urlpatterns = [
    # JWT
    path('jwt/create/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Posts
    path('posts/',
         PostViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='post-list'),
    path('posts/<int:pk>/', PostViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
        'delete':
        'destroy'
    }), name='post-detail'),

    # Comments
    path('posts/<int:post_id>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='comment-list'),
    path('posts/<int:post_id>/comments/<int:pk>/', CommentViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
        'delete': 'destroy'
    }), name='comment-detail'),

    # Groups
    path('groups/', GroupViewSet.as_view({'get': 'list'}), name='group-list'),
    path('groups/<int:pk>/',
         GroupViewSet.as_view({'get': 'retrieve'}), name='group-detail'),

    # Follows
    path('follow/', FollowViewSet.as_view(), name='follow-list'),
]
