from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Department, Employee


@admin.register(Department)
class DepartmentAdmin(MPTTModelAdmin):
    list_display = ('name',)
    list_filter = ('parent',)
    search_fields = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'position',
        'department',
        'hire_date',
        'salary',
    )
    list_filter = ('department', 'position')
    search_fields = ('full_name', 'position')
    date_hierarchy = 'hire_date'
