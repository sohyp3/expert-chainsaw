from django.contrib import admin
from .models import linksModel,pythonUseragentModel,jsUseragentModel

admin.site.register(pythonUseragentModel)
admin.site.register(jsUseragentModel)
