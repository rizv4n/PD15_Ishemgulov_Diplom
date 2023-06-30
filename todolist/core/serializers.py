from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from core.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message='Username is already in use')]
    )
    email = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message='Email is already in use')]
    )
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validate_data):
        password = validate_data.pop('password')
        password_repeat = validate_data.pop('password_repeat')

        if password != password_repeat:
            raise serializers.ValidationError('Passwords dont match')

        user = super().create(validate_data)
        user.set_password(user.password)
        user.save()

        return user


class UserRetrieveSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message='Username is already in use')]
    )
    email = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message='Email is already in use')]
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UpdatePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True)
    old_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password']

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate_old_password(self, old_password):
        return self.context['request'].user.check_password(old_password)

    def save(self, **kwargs):
        user = self.instance
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
