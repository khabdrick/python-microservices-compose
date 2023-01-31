from django.contrib import admin
from blog.models import Article, User

# class UserAdmin(admin.ModelAdmin):
#     readonly_fields = ('id',)

admin.site.register(Article)
admin.site.register(User)
