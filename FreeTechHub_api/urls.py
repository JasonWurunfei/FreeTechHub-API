from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from user.views import WebsocketView
from .views import UploadImgView
from django.views.decorators.csrf import csrf_exempt
# just to signal this is a websocket path
websocket = path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('comment/', include('comment.urls')),
    path('user/', include('user.urls')),
    path('tag/', include('tag.urls')),
    path('question/', include('question.urls')),
    path('transaction/', include('transaction.urls')),
    path('like/', include('like.urls')),
    path('search/', include('search.urls')),
    path('skilltree/', include('skilltree.urls')),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('imgUpload/',UploadImgView.as_view()),
    url(r'^api/login/', include('rest_social_auth.urls_jwt')),

    # Async views
    websocket('ws/', WebsocketView),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
