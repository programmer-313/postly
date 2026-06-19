from django.contrib import admin

from posts.models import (
    Post, 
    PostTag,
    PostImage
)


admin.site.register(Post, admin.ModelAdmin)
admin.site.register(PostTag, admin.ModelAdmin)
admin.site.register(PostImage)
