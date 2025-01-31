from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from projects.models import Project, Contributor
from users.models import User


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ('user', 'project', 'created_time')


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'type', 'author', 'created_time')


class ProjectDetailSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    contributors = SlugRelatedField(queryset=User.objects.all(),
                                    slug_field='username',
                                    many=True, required=False, write_only=True)
    contributors_id = serializers.PrimaryKeyRelatedField(many=True,
                                                         source='contributors',
                                                         read_only=True)


    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'type', 'author', 'created_time',
                  'contributors', 'contributors_id')


    def validate_contributors(self, value):
        instance = self.instance
        if instance:
            author = instance.author
            if author not in value and author in instance.contributors.all():
                raise serializers.ValidationError(
                    "L'auteur du projet doit faire parti des contributeurs.")
        return value


class ProjectCreateSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    contributors = SlugRelatedField(queryset=User.objects.all(),
                                    slug_field='username',
                                    many=True, required=False)


    class Meta:
        model = Project
        fields = ('id',
                  'title', 'description', 'type', 'author', 'created_time',
                  'contributors')


class ProjectUpdateSerializer(serializers.ModelSerializer):
    contributors = SlugRelatedField(queryset=User.objects.all(),
                                    slug_field='username',
                                    many=True,
                                    required=False)


    class Meta:
        model = Project
        fields = (
            'title', 'description', 'type', 'contributors')
