from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


# CRITICAL: NEVER bypass PermissionService for access control.
class BaseScopedViewSet(ModelViewSet):
    def get_queryset(self):
        raise NotImplementedError("Must use PermissionService scoping")


# CRITICAL: NEVER bypass PermissionService for access control.
class BaseScopedReadOnlyViewSet(ReadOnlyModelViewSet):
    def get_queryset(self):
        raise NotImplementedError("Must use PermissionService scoping")