from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
import re
import uuid

from .models import Business # Make sure your models.py is in the same directory or adjust import

def generate_unique_business_id():
    """Generates a unique ID for a business."""
    return "BIZ-" + str(uuid.uuid4()).split("-")[0] # Example: BIZ-3fa85f


class BusinessSerializer(serializers.Serializer): # Removed UserDataValidationMixin
    businesses_id = serializers.IntegerField(read_only=True) # Primary key, read-only
    businesses_unique_id = serializers.CharField(required=False, read_only=True) # Generated on creation
    businesses_user_name = serializers.CharField(
        max_length=255, 
        required=False, 
        allow_blank=True, 
        allow_null=True, 
        trim_whitespace=True,
        help_text="User-defined unique name for the business."
    )
    businesses_legal_name = serializers.CharField(
        max_length=255, 
        required=True, 
        allow_blank=False, 
        trim_whitespace=True,
        help_text="The official legal name of the business. Required."
    )
    businesses_organization_name = serializers.CharField(
        max_length=255, 
        required=False, 
        allow_blank=True, 
        allow_null=True, 
        trim_whitespace=True,
        help_text="The common organization name, if different from legal name."
    )
    businesses_gst_number = serializers.CharField(
        max_length=255, 
        required=False, 
        allow_blank=True, 
        allow_null=True, 
        trim_whitespace=True,
        help_text="Goods and Services Tax (GST) number, if applicable."
    )
    businesses_website = serializers.URLField(
        max_length=255, 
        required=False, 
        allow_blank=True, 
        allow_null=True,
        help_text="Official website URL of the business."
    )
    businesses_documents = serializers.CharField(
        required=False, 
        allow_blank=True, 
        allow_null=True,
        help_text="Text field for storing document references or paths (e.g., JSON string of file paths)."
    )
    businesses_logo = serializers.CharField(
        required=False, 
        allow_blank=True, 
        allow_null=True,
        help_text="Text field for storing logo data (e.g., base64 string or URL)."
    )
    businesses_is_active = serializers.BooleanField(
        required=False, 
        default=True,
        help_text="Indicates if the business is currently active."
    )



    def to_representation(self, instance):
        """
        Custom representation to format the logo field as a data URL if it's a base64 string.
        """
        data = super().to_representation(instance)
        logo = data.get("businesses_logo")

        # Assuming logo is stored as a base64 string without the prefix
        if logo and not logo.startswith("data:image"):
            # You might want to infer the image type, here assuming JPEG for example
            # In a real app, you might store type or validate it.
            data["businesses_logo"] = f"data:image/jpeg;base64,{logo}" # Or dynamically determine type

        return data

    # Custom Validators for specific fields
    def validate_businesses_gst_number(self, value):
        """
        Validates the format of the GST number (Indian GSTIN example).
        Adjust regex based on actual GST/VAT/Tax ID format.
        Example for Indian GSTIN: 15 alphanumeric characters.
        """
        if value:
            # Basic regex for 15 alphanumeric characters (common for Indian GSTIN)
            # This regex needs to be adapted based on the exact format you expect.
            if not re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$', value, re.IGNORECASE):
                raise serializers.ValidationError("Invalid GST number format.")
        return value

    def validate_businesses_user_name(self, value):
        """
        Optional: Add specific validation rules for user name, e.g., no special characters.
        """
        if value and not re.match(r'^[a-zA-Z0-9_.-]+$', value):
            raise serializers.ValidationError("User name can only contain letters, numbers, underscores, dots, or hyphens.")
        return value

    def validate_businesses_legal_name(self, value):
        """
        Optional: Add specific validation rules for legal name.
        """
        if value and not re.match(r'^[a-zA-Z0-9\s.,&()-]+$', value): # Allows letters, numbers, spaces, common punctuation
            raise serializers.ValidationError("Legal name contains invalid characters.")
        return value

    def validate_businesses_organization_name(self, value):
        """
        Optional: Add specific validation rules for organization name.
        """
        if value and not re.match(r'^[a-zA-Z0-9\s.,&()-]+$', value):
            raise serializers.ValidationError("Organization name contains invalid characters.")
        return value

    def create(self, validated_data):
        """
        Overrides the create method to handle unique ID generation.
        """
        try:
            with transaction.atomic():
                # Assign generated unique ID
                validated_data["businesses_unique_id"] = generate_unique_business_id()

                # If you decide to add businesses_created_by field to the model, you'd set it here
                # e.g., validated_data["businesses_created_by"] = self.context['request'].user.username if 'request' in self.context else "system"

                instance = Business.objects.create(**validated_data)
                return instance
        except Exception as e:
            raise serializers.ValidationError(f"Error creating business: {str(e)}")

    def update(self, instance, validated_data):
        """
        Overrides the update method.
        """
        try:
            with transaction.atomic():
                # If you decide to add businesses_updated_by field to the model, you'd set it here
                # e.g., validated_data["businesses_updated_by"] = self.context['request'].user.username if 'request' in self.context else "system"

                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                
                # Update the timestamp manually if auto_now=True is not desired or for explicit control
                # instance.businesses_updated_at = timezone.now() 
                
                instance.save()
                return instance
        except Exception as e:
            raise serializers.ValidationError(f"Error updating business: {str(e)}")