from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ["first_name", "last_name", "email", "password", "is_staff"]
        # password will not be shown
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate_password(self, value):
            try:
                # Django password validators (minimum length, complexity, etc.)
                validate_password(value)  
            except Exception as e:
                raise serializers.ValidationError(str(e))
            return value
    
    # create new hashed instance of password 
    def create(self, validate_data):
        password = validate_data.pop("password", None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            # hashing the password with sha256
            instance.set_password(password)
        instance.save()
        return instance 
    
    # updating password with hashing
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password is not None:
            instance.set_password(password)
        return super().update(instance, validated_data)
    

