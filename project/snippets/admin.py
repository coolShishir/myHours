from django.contrib import admin
# Register your models here.
from models import User,Project,UserLog

admin.site.register(Project)
admin.site.register(User)
admin.site.register(UserLog)

