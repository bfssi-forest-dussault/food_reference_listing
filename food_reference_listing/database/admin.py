from django.contrib import admin
from food_reference_listing.database import models

# Register your models here.
admin.site.register(models.Product)
admin.site.register(models.Company)
admin.site.register(models.Subcategory)
admin.site.register(models.Category)
