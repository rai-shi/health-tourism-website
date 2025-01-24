from rest_framework import serializers

from django.shortcuts import get_object_or_404

from medical_centers.models import MedicalCenter

class MedicalCenterListSerializer(serializers.ModelSerializer):
    """
    MedicalCenterListSerializer can be only used for serializing the MedicalCenter data for its preview 

    return params:
        "id",
        "center_name",
        "center_type",
        "city",
        "contact_number",
        "mail_address",
        "web_site",
        "preview_text"
    """
    city = serializers.SerializerMethodField()
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
    def get_city(self, obj):
        return {
            "id" : obj.city.id,
            "city": obj.city.name
        }