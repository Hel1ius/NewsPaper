from django.urls import path

from . import views


urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('filter/', views.FilterPostView.as_view(), name='filter'),
    path('chapter', views.FilterChapterView.as_view(), name='chapter'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('post/<int:pk>', views.PostDetail.as_view(), name='post_detail'),
    path('comment/<int:pk>/', views.AddComment.as_view(), name='add_comment'),
    path('post/create', views.AddPost.as_view(), name='add_post'),
    path('post/<int:pk>/edit', views.UpdatePost.as_view(), name='update_post'),
    path('post/<int:pk>/delete', views.DeletePost.as_view(), name='delete_post'),
    path('upgrade/', views.upgrade_me, name='upgrade'),
    path('subscribe/<int:pk>/', views.subscribe_to_category, name='subscribe'),
    path('add_sub/', views.AddEmail.as_view(), name='add_sub')
]