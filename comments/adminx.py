import xadmin
from .models import Comment

class CommentAdmin(object):
	list_display = ['name', 'email', 'url', 'text', 'create_time', 'post']
	search_fields = ['name', 'email', 'url']
	list_editable = ['name', 'email', 'url', 'text', 'create_time', 'post']
	list_filter = ['name', 'email', 'url', 'text', 'create_time', 'post']

xadmin.site.register(Comment, CommentAdmin)