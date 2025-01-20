from rest_framework import serializers
from .models import Patient
from .models import MedicalCenterRequest, MedicalCenterRequestFile

class PatientSerializers(serializers.ModelSerializer):
    # return field with their __str__ return 
    country = serializers.StringRelatedField()  
    city = serializers.StringRelatedField()  

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
    

class MedicalCenterRequestFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCenterRequestFile
        fields = ['id', 'file']

class MedicalCenterRequestSerializer(serializers.ModelSerializer):
    # files = MedicalCenterRequestFileSerializer(many=True, required=False)

    class Meta:
        model = MedicalCenterRequest
        fields = [
            'id', 'patient', 'medical_center', 'speciality', 'procedure',
            'name', 'surname', 'gender', 'birthday', 'phone', 'email',
            'country', 'city', 
            'disease_history', 'previous_disease', 'previous_surgery',
            'previous_treatment', 'other_comments', 
            # 'files'
        ]
