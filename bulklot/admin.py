from django.contrib import admin

from .models import LotRequest, LotRequestTime, Member, LotResult

class LotReqTimeInline(admin.TabularInline):
    model = LotRequestTime

class LotReqAdmin(admin.ModelAdmin):
    readonly_fields = ('req_date',)
    fields = ('req_date', 'requester', 'location', 'sport')
    inlines = [LotReqTimeInline]
    list_display = ('req_date', 'requester', 'location', 'sport')

class LotReqTimeAdmin(admin.ModelAdmin):
    list_display = ('lot_request', 'member', 'date', 'time', 'status')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'tmgbc_id', 'tmgbc_password')

class LotResultAdmin(admin.ModelAdmin):
    list_display = ('owner', 'member', 'datetime', 'sport', 'location', 'result', 'pubdate', 'active')

admin.site.register(LotRequest, LotReqAdmin)
admin.site.register(LotRequestTime, LotReqTimeAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(LotResult, LotResultAdmin)

