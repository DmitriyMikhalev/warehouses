from .models import Product, Vehicle


class MaxProductChoiceMixin:
    def get_max_num(self, request, obj=None):
        """
        Disallow to create more rows than products count (additional filter for
        unique) while creating related instance.
        """
        return Product.objects.count()


class MaxVehicleChoiceMixin:
    def get_max_num(self, request, obj=None):
        """
        Disallow to create more rows than vehicle count (additional filter for
        unique) while creating related instance.
        """
        return Vehicle.objects.count()


class NoAddPermissionMixin:
    def has_add_permission(self, request, obj=None):
        return False


class NoChangePermissionMixin:
    def has_change_permission(self, request, obj=None):
        return False


class UnacceptedFilterMixin:
    def get_queryset(self, request):
        """Filters queryset to return only unaccepted instances."""
        return super().get_queryset(request).filter(accepted=False)
