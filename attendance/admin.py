from django.contrib import admin
from attendance.models import Student,AttendanceRecord,New_Commers_Validate,Contact
admin.site.register(Contact)
admin.site.site_header = "Welcome Admin"
admin.site.site_title = "Administration"
admin.site.index_title = "Dashboard"

# Register your models here.
admin.site.register(Student)
admin.site.register(AttendanceRecord)
admin.site.register(New_Commers_Validate)