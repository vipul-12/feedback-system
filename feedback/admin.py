from django.contrib import admin
from .models import Feedback
# Register your models here.

class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'review', 'feedback','date', 'subject', 'punctual', 'audible')

admin.site.register(Feedback, FeedbackAdmin)
