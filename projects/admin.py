from django.contrib import admin

from projects.models import Project, Contributor

class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'author', 'type')
    fields = ('title', 'description', 'type', 'author')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
