from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify

# Create your views here.
class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	paginate_by = 2

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')
		data = self.pagination_data(page, paginator, is_paginated)
		context.update(data)
		return context

	def pagination_data(self, page, paginator, is_paginated):
		if not is_paginated:
			return {}

		left = []
		right = []
		left_has_more = False
		right_has_more = False
		first = False
		last = False

		page_number = page.number
		total_page = paginator.num_pages
		page_range = paginator.page_range

		if page_number == 1:
			right = page_range[page_number:page_number + 2]

			if right[-1] < total_page - 1:
				right_has_more = True

			if right[-1] < total_page:
				last = True

		elif page_number == total_page:
			left = page_range[page_number - 3 if page_number - 3 > 0 else 0: page_number - 1]

			if left[0] > 2:
				left_has_more = True

			if left[0] > 1:
				first = True

		else:
			left = left = page_range[page_number - 3 if page_number - 3 > 0 else 0: page_number - 1]
			right = page_range[page_number:page_number + 2]

			if right[-1] < total_page - 1:
				right_has_more = True

			if right[-1] < total_page:
				last = True

			if left[0] > 2:
				left_has_more = True

			if left[0] > 1:
				first = True

		data = {
			'left': left,
			'right': right,
			'left_has_more': left_has_more,
			'right_has_more': right_has_more,
			'first': first,
			'last': last,
		}
		return data

def detail(request, pk):
	post = get_object_or_404(Post, pk = pk)
	post.increase_views()
	md = markdown.Markdown(extensions = ['markdown.extensions.extra',
				'markdown.extensions.codehilite', TocExtension(slugify = slugify),])
	post.body = md.convert(post.body)
	post.toc = md.toc
	form = CommentForm()
	comment_list = post.comment_set.all()
	context = {'post': post, 'form': form, 'comment_list': comment_list}
	return render(request, 'blog/detail.html', context = context)

class ArchiveView(IndexView):
	
	def get_queryset(self):
		return super(ArchiveView, self).get_queryset().filter(created_time__year = self.kwargs.get('year'),
					created_time__month = self.kwargs.get('month'))

class CategoryView(IndexView):
	
	def get_queryset(self):
		category = get_object_or_404(Category, pk = self.kwargs.get('pk'))
		return super(CategoryView, self).get_queryset().filter(category = category)

class TagView(IndexView):

	def get_queryset(self):
		tag = get_object_or_404(Tag, pk = self.kwargs.get('pk'))
		return super(TagView, self).get_queryset().filter(tag = tag)
