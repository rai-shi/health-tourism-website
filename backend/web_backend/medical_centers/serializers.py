from rest_framework import serializers
from .models import *

from rest_framework import serializers
from .models import *

class MedicalCenterSerializers(serializers.ModelSerializer):
    # Many-to-many ilişkiler için nested serializer'lar eklenebilir
    specialities = serializers.StringRelatedField(many=True)
    procedure = serializers.StringRelatedField(many=True)
    contracted_health_institutions = serializers.StringRelatedField(many=True)
    doctors = serializers.StringRelatedField(many=True)
    medical_center_photos = serializers.StringRelatedField(many=True)
    medical_center_videos = serializers.StringRelatedField(many=True)

    class Meta:
        model = MedicalCenter
        fields = [
            "user",
            "center_name",
            "center_type",
            "city",
            "contact_number",
            "mail_address",
            "web_site",
            "preview_text",
            "overview_text",
            "specialities",  # Many-to-many ilişkiler
            "procedure",  # Many-to-many ilişkiler
            "contracted_health_institutions",  # Many-to-many ilişkiler
            "doctors",  # Many-to-many ilişkiler
            "medical_center_photos",  # Many-to-many ilişkiler
            "medical_center_videos",  # Many-to-many ilişkiler
        ]
        extra_kwargs = {
                
        }
