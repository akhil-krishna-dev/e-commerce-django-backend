from django.contrib import admin
from .models import OrderAddress,Payment,Orders


admin.site.register([OrderAddress,Payment,Orders])
