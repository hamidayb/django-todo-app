from rest_framework.mixins import ListModelMixin


class CurrentUserLookupMixin(ListModelMixin):
    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)
