from django.db import models

# Create your models here.
class Comment(models.Model):
	name = models.CharField(max_length = 50, verbose_name = '姓名')
	email = models.EmailField(max_length = 100, verbose_name = '邮件')
	url = models.URLField(blank = True, verbose_name = '地址')
	text = models.TextField(verbose_name = '评论内容')
	create_time = models.DateTimeField(auto_now_add = True, verbose_name = '创建时间')

	post = models.ForeignKey('blog.Post', verbose_name = '文章')

	def __str__(self):
		return self.text[:20]

	class Meta:
		verbose_name = '评论'
		verbose_name_plural = verbose_name