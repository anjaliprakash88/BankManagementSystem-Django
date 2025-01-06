from django.contrib import admin
from .models import user, CustomUser, Transaction


admin.site.register(user)
admin.site.register(CustomUser)
admin.site.register(Transaction)
