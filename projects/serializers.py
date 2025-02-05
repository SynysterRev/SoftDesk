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
        fields = ('id', 'title', 'type', 'author', 'created_time')


class ProjectDetailSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    contributors = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                      many=True, required=False)


    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'type', 'author', 'created_time',
                  'contributors')


    def create(self, validated_data):
        instance = super().create(validated_data)
        author = instance.author
        if not instance.contributors.filter(id=author.id).exists():
            instance.contributors.add(author)
        return instance

    def validate_contributors(self, value):
        instance = self.instance
        if instance:
            author = instance.author
            if author not in value:
                raise serializers.ValidationError(
                    "L'auteur du projet doit faire parti des contributeurs.")
        return value


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id', 'title', 'author', 'status', 'priority', 'tag', 'assigned_to',
                  'project', 'created_time')


class IssueDetailSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'project_pk': 'project__pk',
    }
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)


    class Meta:
        model = Issue
        fields = ('id', 'title', 'description', 'author', 'status', 'priority', 'tag',
                  'assigned_to', 'project', 'created_time')


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('uuid', 'author', 'issue', 'created_time')


class CommentDetailSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'issue_pk': 'issue__pk',
        'project_pk': 'issue__project__pk',
    }
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    issue = serializers.PrimaryKeyRelatedField(read_only=True)


    class Meta:
        model = Comment
        fields = ('uuid', 'description', 'author', 'issue', 'created_time')
