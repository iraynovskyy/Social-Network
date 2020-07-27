from django.urls import include, path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('welcome/', views.welcome, name="welcome"),
    path('user_signup/', views.user_signup, name="user_signup"),
    path('user_login/', views.user_login, name='user_login'),

    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('post_creation/', views.post_creation, name="post_creation"),
    path('<postid>/preference/<userpreference>/', views.postpreference, name='postpreference'),
    path('analytics/', views.analytics, name='analytics'),
    path('user_activity/<user_id>/', views.user_activity, name='user_activity'),
    path('post_info/', views.post_info, name="post_info"),
]
