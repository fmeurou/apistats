from django.contrib import admin
from django.db import models

from .models import APIStat


class APIStatAdmin(admin.ModelAdmin):
    date_hierarchy = 'record_time'
    list_display = ('record_time', 'method', 'domain', 'path', 'user', 'delay', 'status')
    readonly_fields = ('record_time', 'method', 'domain', 'path', 'delay', 'status',
                       'query', 'ip', 'total_count', 'domain_count', 'path_count',
                       'avg_delay', 'avg_domain_delay', 'avg_path_delay',
                       'max_delay', 'max_domain_delay', 'max_path_delay',)
    list_filter = ('method', 'domain', 'path', 'user')
    fieldsets = (
        (None, {
            'fields': ('record_time', 'domain', 'path', 'user')
        }),
        ('Request', {
            'fields': ('method', 'query', 'ip'),
        }),
        ('Response', {
            'fields': ('delay', 'status'),
        }),
        ('Stats', {
            'fields': ('total_count', 'max_delay', 'avg_delay',
                       'domain_count', 'max_domain_delay', 'avg_domain_delay',
                       'path_count', 'max_path_delay', 'avg_path_delay'),
        }),
    )


admin.site.register(APIStat, APIStatAdmin)


class APIStatPathAgregatedAdmin(admin.ModelAdmin):
    list_display = ('path', 'counter')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.values('path').annotate(counter=models.Count('record_time'))


class Year(models.Func):
    function = 'EXTRACT'
    template = '%(function)s(YEAR from %(expressions)s)'
    output_field = models.IntegerField()


class Month(models.Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


class Day(models.Func):
    function = 'EXTRACT'
    template = '%(function)s(DAY from %(expressions)s)'
    output_field = models.IntegerField()


class APIStatDayAgregatedAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'day', 'counter')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            year=Year('record_time'),
            month=Month('record_time'),
            day=Day('record_time')).values(
            'year', 'month', 'day'
        ).annotate(counter=models.Count('record_time')).order_by('year', 'month', 'day')
