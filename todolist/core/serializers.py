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
    password_repeat = serializers.CharField(max_length=128,
                                            write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate_password_repeat(self, value):
        data = self.initial_data
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError('Passwords dont match')
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        del validated_data['password_repeat']
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
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
        check = self.context['request'].user.check_password(old_password)
        if check:
            return old_password
        else:
            raise serializers.ValidationError('Old password incorrect')

    def save(self, **kwargs):
        user = self.instance
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
