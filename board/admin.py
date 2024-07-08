from django.contrib import admin
from .models import Board 

# Register your models here.

class BoardAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(Board, BoardAdmin)

