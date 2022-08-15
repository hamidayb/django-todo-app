from django.contrib import admin
from .models import Task, User, Time
# Register your models here.
from datetime import datetime
from pytz import timezone


# class CreatedDayFilter(admin.SimpleListFilter):
#     title = 'created day'
#     parameter_name = 'created_day'
#     template = 'base/created.html'

#     def lookups(self, request, model_admin):
#         return (
#             ('3', '3rd August'),
#             ('4', '4th August'),
#             ('5', '5th August'),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == '3':
#             return queryset.filter(
#                 created__gte=date(2022, 8, 3),
#                 created__lte=date(2022, 8, 4),
#             )
#         if self.value() == '4':
#             return queryset.filter(
#                 created__gte=date(2022, 8, 4),
#                 created__lte=date(2022, 8, 5),
#             )
#         if self.value() == '5':
#             return queryset.filter(
#                 created__gte=date(2022, 8, 5),
#                 created__lte=date(2022, 8, 6),
#             )


class CompleteFieldFilter(admin.SimpleListFilter):
    title = 'completion status'
    parameter_name = 'complete_filter'

    def lookups(self, request, model_admin):
        return (
            ('completed', 'Completed'),
            ('incomplete', 'InComplete'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'completed':
            return queryset.filter(
                complete=True
            )
        if self.value() == 'incomplete':
            return queryset.filter(
                complete=False
            )


def mark_complete(modeladmin, request, queryset):
    queryset.update(complete=True)


def mark_incomplete(modeladmin, request, queryset):
    queryset.update(complete=True)


@admin.register(Task)
class TaskAdminView(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'title', 'description',
                    'complete', 'created', 'updated']

    @admin.display(description="full name")
    def full_name(self, obj):
        return obj.user

    # inlines = [TaskInline]

    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('complete',),
            'description': 'Do not check it if you haven\'t completed the task',
        }),
    )
    exclude = []
    actions = [mark_complete, mark_incomplete]
    actions_on_bottom = True
    actions_on_top = False
    actions_selection_counter = True
    date_hierarchy = 'created'
    list_filter = [('user', admin.RelatedOnlyFieldListFilter),
                   CompleteFieldFilter]
    search_fields = ['title__startswith', 'description']


@admin.register(User)
class UserAdminView(admin.ModelAdmin):
    list_display = ['id', 'email', 'name', 'age', 'city', 'country', 'created']
    list_editable = ['city', ]
    list_display_links = ['email', ]
    date_hierarchy = 'created'
    list_filter = [
        ('city', admin.EmptyFieldListFilter),
    ]


@admin.register(Time)
class TimeAdminView(admin.ModelAdmin):
    list_display = ['id', 'time', 'timezone']
    # @admin.display(description="time")
    # def _time(self, obj):
    #     if(obj.timezone == "PST"):
    #         datetime_obj = datetime.strptime(obj.time, "%d-%m-%y %H:%M:%S")
    #         datetime_obj_utc = datetime_obj.replace(tzinfo=timezone('UTC'))
    #         print(datetime_obj_utc)
    #         return datetime_obj_utc.strftime("%d-%m-%y %H:%M:%S")
    #     else:
    #         datetime_obj = datetime.strptime(obj.time, "%d-%m-%y %H:%M:%S")
    #         datetime_obj_utc = datetime_obj.replace(tzinfo=timezone('US/Pacific'))
    #         print(datetime_obj_utc)
    #         return datetime_obj_utc.strftime("%d-%m-%y %H:%M:%S")


# Following method can also be used to register models
# admin.site.register(Task, TaskView)
# admin.site.register(User, UserAdminView)
