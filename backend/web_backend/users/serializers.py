from rest_framework import serializers
from .models import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ["id", "first_name", "last_name", "email", "password"]
        # password will not be shown
        extra_kwargs = {
            "password": {"write_only": True}
        }

    # hashing the password with sha256
    # password validation
    def create(self, validate_data):
        password = validate_data.pop("password", None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance 
    

