from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('blog', views.BlogViewSet)
router.register('series', views.SeriesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('query-related-content/', views.QueryView.as_view()),
    path('update_selected_items/', views.UpdateSelectedView.as_view()),
    path('query-related-blogAndSeries/', views.QueryRelatedBlogAndSeriesView.as_view()),
]
