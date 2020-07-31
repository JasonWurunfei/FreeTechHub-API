from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('user/', include('user.urls')),
    path('tag/', include('tag.urls')),
    path('question/', include('question.urls')),
    path('transaction/', include('transaction.urls')),
    path('like/', include('like.urls')),
    
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-verify/', verify_jwt_token),
]
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]