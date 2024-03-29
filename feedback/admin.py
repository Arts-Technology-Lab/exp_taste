from django.contrib import admin

from feedback.models import Question, PageCopy, MultiChoiceOption

@admin.display(description="Text")
def truncated_text(obj, max_length=40):
    return obj.text[:max_length]


class MultiChoiceInline(admin.TabularInline):
    model = MultiChoiceOption
    extra = 1
    fields = ('order', 'text2', 'weight')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ('order', 'text', 'active', 'qtype', 'required')
    list_display = (truncated_text, 'required', 'order')
    list_editable = ('required', 'order')
    inlines = [MultiChoiceInline]

    class Media:
        js = ("js/question.js",)

@admin.register(PageCopy)
class PageCopyAdmin(admin.ModelAdmin):
    list_display = (truncated_text, 'current')
    list_editable = ('current',)

    

