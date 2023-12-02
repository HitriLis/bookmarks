from django.utils.decorators import method_decorator
from django.http import Http404

from rest_framework import viewsets, generics, mixins, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from .serializers import (
    CollectionBookmarksCreateSerializer,
    CollectionBookmarksDetailSerializer,
    CollectionBookmarksSerializer, CollectionAddBookmarksSerializer, BookmarksDetailSerializer,
    BookmarksUpdateSerializer, BookmarksListSerializer
)
from ..models import CollectionBookmarks, Bookmarks


class CollectionBookmarksView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = CollectionBookmarks.objects.filter(user=user).prefetch_related('bookmarks').all()
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CollectionBookmarksCreateSerializer
        return CollectionBookmarksSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.validated_data['user'] = user
        instance = serializer.save()
        return instance

    @extend_schema(
        tags=['Collection'],
        description="Collection list"
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=['Collection'],
        description="Collection create"
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CollectionBookmarksDetailView(mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin,
                                    mixins.RetrieveModelMixin,
                                    generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = CollectionBookmarks.objects.filter(user=user).prefetch_related('bookmarks').all()
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CollectionBookmarksCreateSerializer
        return CollectionBookmarksDetailSerializer

    @extend_schema(
        tags=['Collection'],
        description="Collection detail"
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    @extend_schema(
        tags=['Collection'],
        description="Collection update"
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=['Collection'],
        description="Delete collection"
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CollectionAddBookmarksDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            user = self.request.user
            return CollectionBookmarks.objects.get(id=pk, user=user)
        except Exception as e:
            raise Http404

    @extend_schema(
        tags=['Collection'],
        description="Collection add bookmarks",
        request=CollectionAddBookmarksSerializer,
    )
    def put(self, request, pk):
        collection = self.get_object(pk)
        serializer = CollectionAddBookmarksSerializer(data=request.data)

        if serializer.is_valid():
            serializer_data = serializer.validated_data
            bookmarks_id = serializer_data['bookmarks_id']
            collection.bookmarks.add(bookmarks_id)
            collection.save()

            return Response(CollectionBookmarksDetailSerializer(collection).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookmarksDetailView(mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.RetrieveModelMixin,
                          generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Bookmarks.objects.filter(user=user).select_related('link_type').prefetch_related('collection').all()
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return BookmarksUpdateSerializer
        return BookmarksDetailSerializer

    @extend_schema(
        tags=['Bookmarks'],
        description="Bookmarks detail"
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    @extend_schema(
        tags=['Bookmarks'],
        description="Bookmarks update"
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=['Bookmarks'],
        description="Delete bookmarks"
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@method_decorator(name="get", decorator=extend_schema(
    tags=['Bookmarks'],
    responses={
        status.HTTP_200_OK: BookmarksUpdateSerializer,
    },
    description="Bookmarks list"
))
class BookmarksListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    # filter_backends = [DjangoFilterBackend]
    # filterset_class = PublicTrainingFilter
    # pagination_class = StandardResultsSetPagination
    serializer_class = BookmarksListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Bookmarks.objects.filter(user=user).select_related('link_type').prefetch_related('collection').all()
        return queryset
