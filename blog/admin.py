from django.contrib import admin
from blog.models import Post, Tag, Comment


class PostAdmin(admin.ModelAdmin):
    search_fields = [
        "title",
    ]
    list_display = ["title", "slug", "published_at"]
    list_filter = ["published_at", "title"]
    raw_id_fields = ("likes", "tags", "author")


class CommentAdmin(admin.ModelAdmin):
    search_fields = [
        "text",
    ]
    list_display = ["id", "published_at"]
    list_filter = ["published_at", "text"]
    raw_id_fields = (
        "post",
        "author",
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
