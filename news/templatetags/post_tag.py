from django import template

from news.models import Category, Post

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_popular_post():
    return Post.objects.filter(draft=False).order_by('-rating')[:5]
