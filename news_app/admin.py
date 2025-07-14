from django.contrib import admin

from .models import News, Category, Contact, Comment

# Register your models here.

# admin.site.register(News)
# admin.site.register(Category)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'publish_time', 'status']
    list_filter = [ 'publish_time', 'status', 'created_time']
    prepopulated_fields = {'slug': ('title',)} # titlega nima yozilsa, slugga ham avtamatik tarzda shu yoziladi
    date_hierarchy = 'publish_time'
    search_fields = ['title', 'body']
    ordering = ('status', 'publish_time')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", 'name']

admin.site.register(Contact)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter =  ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['disabled_comments', 'activate_comments']

    def disabled_comments(self, request, queryset):
        queryset.update(active=False)

    def activate_comments(self, request, queryset):
        queryset.update(active=True)

