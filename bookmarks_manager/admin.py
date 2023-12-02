from django.contrib import admin
from bookmarks_manager.models import LinkType, CollectionBookmarks, Bookmarks


class LinkTypeAdmin(admin.ModelAdmin):
    model = LinkType


admin.site.register(LinkType, LinkTypeAdmin)

class CollectionBookmarksAdmin(admin.ModelAdmin):
    model = CollectionBookmarks


admin.site.register(CollectionBookmarks, CollectionBookmarksAdmin)

class BookmarksAdmin(admin.ModelAdmin):
    model = Bookmarks


admin.site.register(Bookmarks, BookmarksAdmin)
