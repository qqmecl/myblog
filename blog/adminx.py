import xadmin
from .models import Post, Category, Tag

class PostAdmin(object):
    list_display = ['title', 'excerpt', 'created_time', 'modified_time', 'category', 'tag', 'author', 'views']
    search_fields = ['category', 'tag']
    list_editable = ['title', 'created_time', 'modified_time', 'category', 'tag', 'author', 'views']
    list_filter = ['created_time', 'modified_time', 'category', 'tag', 'author', 'views']

class CategoryAdmin(object):
    list_display = ['name']
    list_editable = ['name']
    list_filter = ['name']

class TagAdmin(object):
    list_display = ['name']
    list_editable = ['name']
    list_filter = ['name']
 
class GlobalSetting(object):
    site_title = "chan的后台管理系统"
    site_footer = "http://www.chenli.work"
 
xadmin.site.register(xadmin.views.CommAdminView, GlobalSetting)
xadmin.site.register(Post, PostAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Tag, TagAdmin)