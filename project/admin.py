from django.contrib import admin
from .models import Client, Project, Team

# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name', 'email')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'start_date', 'end_date', 'price', 'status', 'client')
    list_filter = ('status', 'department')
    search_fields = ('name', 'client__name', 'department')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('project', 'leader', 'members_list')
    
    def members_list(self, obj):
        return ", ".join([member.name for member in obj.members.all()])
    members_list.short_description = 'Members'

# Register the models with custom admin classes
admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Team, TeamAdmin)
