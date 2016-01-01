from django.core.paginator import *

def paginatePosts(postList, numberOfResults=10, page=1):
	paginator = Paginator(postList, 10)

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	return posts