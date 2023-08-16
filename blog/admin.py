from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'views', 'publish_date')
    search_fields = ('title', 'content')
    list_filter = ('publish_date',)
