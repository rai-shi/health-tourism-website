from rest_framework import serializers
from .models import Patient

class PatientSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Patient
        fields = [
                  "id",     # Primary Key 
                  "user",   # Relation to user model
                  "gender", 
                  "birthday", 
                  "phone_number", 
                  "country", 
                  "city",
                  "created_at"
                ]
        extra_kwargs = {
            "created_at": {"read_only": True},  # read-only
        }
    
