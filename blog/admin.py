from django.contrib import admin

from blog.models import Post, Person

# Register your models here.
admin.site.register(Post)
admin.site.register(Person)