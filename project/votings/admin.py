from django.contrib import admin
from .models import Author, Question, Choice

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['topic']}),
        ('Date information', {'fields': ['cr_date'],
                              'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('topic', 'cr_date', 'access_token')


admin.site.register(Question, QuestionAdmin)
