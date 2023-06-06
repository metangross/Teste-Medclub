from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def save(self):
        password = self.validated_data.pop("password", None)
        if password:
            password = make_password(password)
            self.validated_data.update({"password": password})
        return super().save()
