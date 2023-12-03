from rest_framework import serializers
from bookmarks_manager.models import CollectionBookmarks, Bookmarks


class BookmarksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmarks
        fields = ['id', 'link_page', 'type', 'type_name', 'page_title']


class CollectionBookmarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionBookmarks
        fields = ['id', 'name', 'short_description']


class CollectionBookmarksCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionBookmarks
        fields = ['id', 'name', 'short_description']


class CollectionAddBookmarksSerializer(serializers.Serializer):
    bookmarks_id = serializers.IntegerField()

    def validate_bookmarks_id(self, value):
        if not Bookmarks.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Закладка не найдена.')
        return value


class CollectionBookmarksDetailSerializer(serializers.ModelSerializer):
    bookmarks = BookmarksListSerializer(many=True)

    class Meta:
        model = CollectionBookmarks
        fields = ['id', 'name', 'short_description', 'bookmarks', 'created_at', 'updated_at']


class BookmarksDetailSerializer(serializers.ModelSerializer):
    collection = CollectionBookmarksSerializer(many=True)

    class Meta:
        model = Bookmarks
        fields = [
            'id',
            'page_title',
            'collection',
            'link_page',
            'type',
            'type_name',
            'short_description',
            'picture',
            'created_at',
            'updated_at'
        ]


class BookmarksCreateSerializer(serializers.Serializer):
    url = serializers.URLField()
