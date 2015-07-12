from zope.interface import implementer

from pyramid.interfaces import IAuthorizationPolicy

from pyramid.location import lineage

from pyramid.compat import is_nonstr_iter

from pyramid.security import (
    ACLAllowed,
    ACLDenied,
    Allow,
    Deny,
    Everyone,
    )

from .models import (
    User,
    )


from sqlalchemy.exc import DBAPIError

import logging


log = logging.getLogger(__name__)


def groupfinder(username, request):
    user = User.find_by_name(username)
    if user is not None:
        return User.group

    return None