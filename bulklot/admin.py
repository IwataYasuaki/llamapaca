from django.contrib import admin

from .models import LotRequest, LotRequestTime

class LotReqTimeInline(admin.TabularInline):
    model = LotRequestTime

class LotReqAdmin(admin.ModelAdmin):
    readonly_fields = ('req_date',)
    fields = ('req_date', 'location')
    inlines = [LotReqTimeInline]
    list_display = ('req_date', 'location')

class LotReqTimeAdmin(admin.ModelAdmin):
    list_display = ('lot_request', 'date', 'time')

admin.site.register(LotRequest, LotReqAdmin)
admin.site.register(LotRequestTime, LotReqTimeAdmin)

