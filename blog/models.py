from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length = 100, verbose_name = '类名')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '分类'
		verbose_name_plural = verbose_name

class Tag(models.Model):
	name = models.CharField(max_length = 100, verbose_name = '标签名')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '标签'
		verbose_name_plural = verbose_name

class Post(models.Model):
	title = models.CharField(max_length = 70, verbose_name = '标题')
	body = models.TextField(verbose_name = '内容')
	created_time = models.DateTimeField(verbose_name = '创建时间')
	modified_time = models.DateTimeField(verbose_name = '修改时间')
	excerpt = models.CharField(max_length = 200, blank = True, verbose_name = '摘要')
	category = models.ForeignKey(Category, verbose_name = '类名')
	tag = models.ManyToManyField(Tag, blank = True, verbose_name = '标签')
	author = models.ForeignKey(User, verbose_name = '作者')
	views = models.PositiveIntegerField(default = 0, verbose_name = '阅读量')

	def get_absolute_url(self):
		return reverse('blog:detail', kwargs={'pk': self.pk})

	def increase_views(self):
		self.views += 1
		self.save(update_fields = ['views'])

	def save(self, *args, **kwargs):
		if not self.excerpt:
			body = markdown.markdown(self.body, extensions = ['markdown.extensions.extra',
						'markdown.extensions.codehilite',])
			self.excerpt = strip_tags(body)[:54]

		super(Post, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-created_time']
		verbose_name = '文章'
		verbose_name_plural = verbose_name