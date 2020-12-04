import logging
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError, SuspiciousOperation
from django.core.validators import validate_integer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from messagebus.serializer import MessageBusSerializer


logger = logging.getLogger(__name__)


class MessageBusViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MessageBusSerializer
    http_method_names = ('get',)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Return current user info only
        """
        try:
            id = self.request.GET.get("id")
            # why `int(id)` is not enough: int(3.14) - doesn't raise an exception
            validate_integer(id)
            id = int(id)
        except ValidationError:
            logger.error('"id" parameter is mandatory and must be an integer: id=%r' % self.request.GET.get("id"))
            raise SuspiciousOperation

        if self.request.user.id != id:
            logger.error(f'current_user={self.request.user.id} is not allowed to view user_id={id} info')
            raise PermissionDenied

        return self.queryset.filter(id=id)
