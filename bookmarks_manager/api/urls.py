from django.urls import path

from .views import (
    CollectionBookmarksView,
    CollectionBookmarksDetailView,
    CollectionAddBookmarksDetailView,
    BookmarksDetailView,
    BookmarksListView
)

urlpatterns = [
    path('collection/<int:pk>/', CollectionBookmarksDetailView.as_view(), name='collection'),
    path('collection/', CollectionBookmarksView.as_view(), name='collection-detail'),
    path('collection/<int:pk>/add-bookmark/', CollectionAddBookmarksDetailView.as_view(),
         name='collection-add-bookmark'),
    path('bookmark/', BookmarksListView.as_view(), name='bookmark'),
    path('bookmark/<int:pk>/', BookmarksDetailView.as_view(), name='bookmark-detail'),
]
