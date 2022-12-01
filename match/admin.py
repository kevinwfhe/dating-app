from django.contrib import admin
from .models import Winks, Reject, Match, Date
# Register your models here.
admin.site.register(Winks)
admin.site.register(Match)
admin.site.register(Date)