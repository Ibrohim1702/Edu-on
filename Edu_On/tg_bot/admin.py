from django.contrib import admin
from .models import Sub, Category, Course, Videos


# Register your models here.

class SubVideoAdmin(admin.StackedInline):
    model = Videos


class SubAdmin(admin.ModelAdmin):
    inlines = [SubVideoAdmin]

    class Meta:
        model = Sub


admin.site.register(Sub, SubAdmin)
admin.site.register(Category)
admin.site.register(Course)