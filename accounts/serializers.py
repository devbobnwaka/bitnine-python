from rest_framework import serializers
from accounts.models import (
                                User,
                            )



class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    first_name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    last_name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    has_accepted_terms = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email','has_accepted_terms','password', 'password2']
        extra_kwargs = {
            'first_name ': {'required': True},
            'last_name ': {'required': True},
            'email ': {'required': True},
            'has_accepted_terms ': {'required': True},
            'password' : {'write_only': True},
        }

    def validate(self, data):
        """
        Check that the password match.
        """
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Password does not match")
        return data

    def validate_has_accepted_terms(self, value):
        if not value:
            raise serializers.ValidationError("Terms and condition field is not checked")

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 from validated_data
        user = User.objects.create_user(**validated_data)
        return user