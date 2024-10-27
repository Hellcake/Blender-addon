from django.contrib import admin
from .models import SceneSave

@admin.register(SceneSave)
class SceneSaveAdmin(admin.ModelAdmin):
    list_display = ('username', 'timestamp', 'file_path')
    list_filter = ('username', 'timestamp')
    search_fields = ('username', 'file_path')