from rest_framework import serializers

from .models import User


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
