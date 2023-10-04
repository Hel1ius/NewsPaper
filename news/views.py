from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import Post, Category, Author
from .forms import CommentForm, PostForm, NewsletterForm


# Вывод всех постов на главную страницу
class PostList(Category, ListView):
    model = Post
    queryset = Post.objects.filter(draft=False)
    ordering = '-time_in'
    template_name = 'post/posts_list.html'
    context_object_name = 'post_list'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        return context


# Вывод детальной информации о посте
class PostDetail(DetailView):
    model = Post
    template_name = 'post/posts_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.id:
            user = self.request.user
            post = context['post']
            post_categories = post.categories.all()
            context['is_not_subscribed'] = not Category.objects.filter(pk__in=post_categories, subscribers=user).exists()
            context['is_premium'] = self.request.user.groups.filter(name='author').exists()
        return context


# Добавление комментария под постом
class AddComment(View):
    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Post.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.post = post
            form.save()
        return redirect(post.get_absolute_url())


# Фильтр категорий, которые есть на основной странице
class FilterPostView(Category, ListView):
    template_name = 'post/posts_list.html'

    def get_queryset(self):
        queryset = Post.objects.filter(categories=self.request.GET.get('category'))
        return queryset


# Фильтр news/article основной страницы
class FilterChapterView(Post, ListView):
    template_name = 'post/posts_list.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = Post.objects.filter(chapter=self.request.GET.get('chapter'))
        return queryset


# Поиск на основной странице
class SearchView(ListView):
    paginate_by = 8
    template_name = 'post/posts_list.html'

    def get_queryset(self):
        return Post.objects.filter(header__icontains=self.request.GET.get('q'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


# Добавление нового поста
class AddPost(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('news.add_post',)

    def get(self, request):
        form = PostForm()
        return render(request, 'post/post_create.html', {'form': form})

    def post(self, request, *args):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            # Автозаполнение автора
            form.author = Author.objects.get(user_id=self.request.user.id)
            form.save()
        return redirect(Post.get_absolute_url(form))


class UpdatePost(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    form_class = PostForm
    template_name = 'post/post_create.html'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_editing'] = True
        return context


class DeletePost(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post/post_delete.html'
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        premium_group.user_set.add(user)
    return redirect('/')


@login_required
def subscribe_to_category(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    for category in post.categories.all():
        category.subscribers.add(user)
    return redirect(Post.get_absolute_url(post))


class AddEmail(View):
    def post(self, request):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')