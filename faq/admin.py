  
from django.contrib import admin
from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_en', 'created_at')
    search_fields = ('question_en', 'question_hi', 'question_bn')
    fieldsets = (
        ('English', {'fields': ('question_en', 'answer_en')}),
        ('Hindi', {'fields': ('question_hi', 'answer_hi')}),
        ('Bengali', {'fields': ('question_bn', 'answer_bn')}),
    )
