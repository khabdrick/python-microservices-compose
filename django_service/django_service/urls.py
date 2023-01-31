from django.contrib import admin
from django.urls import path
from blog.views import BlogView, RandomUserView

urlpatterns = [
    path("admin/", admin.site.urls),
        path('blog', BlogView.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('blog/<str:pk>', BlogView.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),
    path('user', RandomUserView.as_view())
]