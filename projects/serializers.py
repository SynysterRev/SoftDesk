from django.urls import reverse
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from projects.models import Project, Issue, Comment
from users.models import User


class ContributorsSlugRelatedField(SlugRelatedField):
    def get_queryset(self):
        issue = self.parent.instance
        if issue:
            project = issue.project
            return project.contributors.all()
        return super().get_queryset()


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "title", "type", "author", "created_time")


class ProjectDetailSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    contributors = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )

    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "description",
            "type",
            "author",
            "created_time",
            "contributors",
        )

    def create(self, validated_data):
        instance = super().create(validated_data)
        author = instance.author
        if not instance.contributors.filter(id=author.id).exists():
            instance.contributors.add(author)
        return instance

    def update(self, instance, validated_data):
        updated_instance = super().update(instance, validated_data)
        author = updated_instance.author
        if not updated_instance.contributors.filter(id=author.id).exists():
            updated_instance.contributors.add(author)
            updated_instance.save()
        return updated_instance

    # def validate_contributors(self, value):
    #     instance = self.instance
    #     if instance:
    #         author = instance.author
    #         if author not in value:
    #             raise serializers.ValidationError(
    #                 "L'auteur du projet doit faire parti des contributeurs.")
    #     return value


class IssueListSerializer(serializers.ModelSerializer):
    # project = serializers.HyperlinkedModelSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = (
            "id",
            "title",
            "author",
            "status",
            "priority",
            "tag",
            "assigned_to",
            "project",
            "created_time",
        )


class IssueDetailSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        "project_pk": "project__pk",
    }
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    project = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Issue
        fields = (
            "id",
            "title",
            "description",
            "author",
            "status",
            "priority",
            "tag",
            "assigned_to",
            "project",
            "created_time",
        )

    def get_project(self, instance):
        project_url = reverse("project-detail", kwargs={"pk": instance.project.id})
        return {
            "id": instance.project.id,
            "url": self.context.get("request").build_absolute_uri(project_url),
        }


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("uuid", "author", "issue", "created_time")


class CommentDetailSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        "issue_pk": "issue__pk",
        "project_pk": "issue__project__pk",
    }
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    issue = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ("uuid", "description", "author", "issue", "created_time")

    def get_issue(self, instance):
        issue_url = reverse(
            "issue-detail",
            kwargs={"project_pk": instance.issue.project.id, "pk": instance.issue.id},
        )
        return {
            "id": instance.issue.id,
            "url": self.context.get("request").build_absolute_uri(issue_url),
        }
