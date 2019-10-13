from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

    def _user(self):
        if 'user' in self.context:
            return self.context['user']

        return self.context['request'].user


class UserCreateSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True,
                                     validators=[UniqueValidator(
                                         queryset=User.objects.all())]
                                     )

    email = serializers.EmailField(write_only=True,
                                   validators=[UniqueValidator(
                                               queryset=User.objects.all())]
                                   )

    def validate_password(self, value):
        # Will throw exception if there are errors
        password_validation.validate_password(value)
        return value

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        user.save()

        return user
