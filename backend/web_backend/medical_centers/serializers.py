from rest_framework import serializers
from .models import *

class MedicalCenterSerializer(serializers.ModelSerializer):
    specialities = serializers.SerializerMethodField()
    procedures = serializers.SerializerMethodField()
    contracted_health_institutions = serializers.SerializerMethodField()

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
            "specialities",
            "procedures",
            "contracted_health_institutions",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def get_specialities(self, obj):
        return [speciality.name for speciality in obj.specialities.all()]

    def get_procedures(self, obj):
        return [procedure.name for procedure in obj.procedures.all()]

    def get_contracted_health_institutions(self, obj):
        return [institution.name for institution in obj.contracted_health_institutions.all()]





class UpdateMedicalCenterSerializer(serializers.ModelSerializer):
    specialities = serializers.ListField(
        child=serializers.IntegerField(), required=True
    )
    procedures = serializers.ListField(
        child=serializers.IntegerField(), required=True
    )
    contracted_health_institutions = serializers.ListField(
        child=serializers.IntegerField(), required=True
    )

    class Meta:
        model = MedicalCenter
        fields = [
            "center_name", "center_type", "city", "contact_number",
            "mail_address", "web_site", "preview_text", "overview_text",
            "specialities", "procedures", "contracted_health_institutions",
        ]

    def validate_contact_number(self, value):
        if not value.startswith("+90"):
            raise serializers.ValidationError("Phone number must be a valid Turkish number.")
        return value

