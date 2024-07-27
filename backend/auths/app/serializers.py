from rest_framework import serializers

from .models import (
	User,
	AuthCode,
)


class RegistrationSerializer(serializers.ModelSerializer):
	"""
	Serializer for registrataion post-method.
	"""

	confirm_password: str = serializers.CharField(
		min_length=7, max_length=128, write_only=True
	)

	class Meta:
		model = User
		exclude = ('is_active', 'is_staff', 'is_superuser')

	def create(self, validated_data):
		validated_data.pop('confirm_password')

		return User.objects.create_user(**validated_data)


class RestorePasswordSerializer(serializers.Serializer):
	"""
	Serializer for sending restore code to user.
	"""

	email: str = serializers.EmailField()


class AuthCodeSerializer(serializers.ModelSerializer):
	"""
	Serializer for activating codes.
	"""

	email: str = serializers.CharField(write_only=True)

	class Meta:
		model = AuthCode
		exclude = ('user', 'expires_at')
