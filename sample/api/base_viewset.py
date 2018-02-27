from django.db.models import QuerySet
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from sample.api.permissions import ValidParentPKPermission


class NestedModelViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    parent_lookup = 'parent'
    parent_pk = None
    parent_queryset = None

    def get_parent_queryset(self):
        assert self.parent_queryset is not None, (
            "'%s' should either include a `parent_queryset` attribute, "
            "or override the `get_parent_queryset()` method."
            % self.__class__.__name__
        )

        parent_queryset = self.parent_queryset
        if isinstance(parent_queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            parent_queryset = parent_queryset.all()
        return parent_queryset

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [ValidParentPKPermission, ]
        permission_classes.extend(self.permission_classes)
        return [permission() for permission in permission_classes]

    def is_valid_parent_pk(self):
        parent_queryset = self.get_parent_queryset()

        if self.parent_pk is not None and parent_queryset.filter(id=self.parent_pk).exists():
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        # get parent_pk from url arguments
        self.parent_pk = kwargs.get('%s_pk' % self.parent_lookup)
        return super(NestedModelViewSet, self).dispatch(request, *args, **kwargs)
