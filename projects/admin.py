from django.contrib import admin

from projects.models import Project, Contributor, Issue, Comment


class ContributorAdmin(admin.ModelAdmin):
    list_display = ("user", "project", "created_time")


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "author", "type", "created_time")


class IssueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "description",
        "status",
        "priority",
        "tag",
        "assigned_to",
        "author",
        "project",
        "created_time",
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ("uuid", "description", "issue", "author", "created_time")


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
