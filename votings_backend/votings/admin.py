from django.contrib import admin
from .models import Question, Choice, Report
from django.contrib.auth.models import User

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['topic', 'description']}),
        ('Date information', {'fields': ['cr_date'],
                              'classes': ['collapse']}),
        ('Author', {'fields': ['author']})
    ]
    inlines = [ChoiceInline]
    list_display = ('topic', 'cr_date', 'access_token', 'public')


class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'email')
    list_display = ('username', 'email', 'is_staff', 'is_active')

class ReportAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Report information', {'fields': ['description', 'question', 'user']}),
    ]
    list_display = ('description', 'question', 'user')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Report, ReportAdmin)
