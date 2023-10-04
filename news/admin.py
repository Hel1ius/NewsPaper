from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Category, Author, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ('user',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('header', 'rating', 'author', 'draft')
    list_filter = ('categories', 'chapter')
    search_fields = ('header', 'categories__name')
    inlines = [CommentInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'parent', 'post')
    readonly_fields = ('user',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="50" height="50"')

    get_image.short_description = 'Изображение'


admin.site.site_title = 'News Paper'
admin.site.site_header = 'News Paper'