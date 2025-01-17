from rest_framework import serializers

from django.shortcuts import get_object_or_404

from medical_centers.models import MedicalCenter

class MedicalCenterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCenter
        fields = [
            "id",
            "center_name",
            "center_type",
            "city",
            "contact_number",
            "mail_address",
            "web_site",
            "preview_text"
        ]