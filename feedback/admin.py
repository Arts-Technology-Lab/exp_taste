from django.contrib import admin

from feedback.models import Question, PageCopy, MultiChoiceOption

@admin.display(description="Text")
def truncated_text(obj, max_length=20):
    return obj.text[:max_length]


class MultiChoiceInline(admin.TabularInline):
    model = MultiChoiceOption
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ('order', 'text', 'active', 'qtype')
    list_display = (truncated_text, 'order')
    list_editable = ('order',)
    inlines = [MultiChoiceInline]

    class Media:
        js = ("js/question.js",)

@admin.register(PageCopy)
class PageCopyAdmin(admin.ModelAdmin):
    list_display = (truncated_text, 'current')
    list_editable = ('current',)

    

