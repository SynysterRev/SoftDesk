from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "can_be_contacted",
            "can_data_be_shared",
            "age",
        )

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            can_be_contacted=validated_data["can_be_contacted"],
            can_data_be_shared=validated_data["can_data_be_shared"],
            age=validated_data["age"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError(
                "Vous devez avoir au moins 15 ans pour " "vous inscrire."
            )
        return value
