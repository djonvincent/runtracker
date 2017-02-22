from django.contrib import admin
from .models import Run
from .models import UserInfo

class RunAdmin(admin.ModelAdmin):
   list_display = ("user", "date", "distance", "duration", "pace")
   
admin.site.register(Run, RunAdmin)
admin.AdminSite.site_header = "RunTracker Admin"

admin.site.register(UserInfo)
