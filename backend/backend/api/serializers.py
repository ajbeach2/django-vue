from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ("user_id", "phone_number")


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    def update(self, instance, validated_data):
        profile_attrs = validated_data.get("profile", None)
        profile = instance.profile

        if profile_attrs is not None:
            for attr, value in profile_attrs.items():
                setattr(profile, attr, value)
            profile.save()

        return instance

    class Meta:
        model = User
        fields = ("id", "email", "profile")
        read_only_fields = ('id')
