from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'can_be_contacted',
                  'can_data_be_shared', 'age')


    def validate(self, data):
        if data['age'] <= 15:
            raise serializers.ValidationError("You must have at least 15 years old to "
                                             "share your data.")
        return data