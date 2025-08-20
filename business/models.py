from django.db import models

class Business(models.Model):
    businesses_id = models.AutoField(primary_key=True) # This field will store the unique id of the business
    businesses_unique_id = models.CharField(max_length=255, unique=True, null=True, blank=True) # This field will store the unique ID of the business
    businesses_user_name = models.CharField(max_length=255, unique=True, null=True, blank=True) # This field will store the user-defined name for the business
    businesses_legal_name = models.CharField(max_length=255, unique=True, null=True, blank=True) # This field will store the legal name of the business
    businesses_organization_name = models.CharField(max_length=255, unique=True, null=True, blank=True) # This field will store the organization name of the business
    businesses_gst_number = models.CharField(max_length=255, unique=True, null=True, blank=True) # This field will store the GST number of the business
    businesses_website = models.CharField(max_length=255, null=True, blank=True) # This field will store the website URL of the business
    businesses_documents = models.TextField(null=True, blank=True) # This field will store paths or references to business documents
    businesses_logo = models.TextField(null=True, blank=True) # This field will store the path or reference to the business logo
    businesses_is_active = models.BooleanField(default=True) # This field indicates if the business record is active
    businesses_is_deleted = models.BooleanField(default=False) # This field indicates if the business record has been soft-deleted
    businesses_created_at = models.DateTimeField(auto_now_add=True) # This field will store the timestamp when the business record was created
    businesses_updated_at = models.DateTimeField(auto_now=True) # This field will store the timestamp when the business record was last updated

    class Meta:
        db_table = 'businesses'