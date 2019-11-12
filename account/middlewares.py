# -*- coding: utf-8 -*-
"""Login middleware."""

from django.contrib.auth import authenticate
from django.middleware.csrf import get_token as get_csrf_token
from conf.default import DEBUG

from account.accounts import Account


class LoginMiddleware(object):
    """Login middleware."""

    def process_view(self, request, view, args, kwargs):
        # if DEBUG:
        #     request.user.username = 'admin'
        #     request.user.is_superuser = True
        #     return None

        """process_view."""
        if getattr(view, 'login_exempt', False):
            return None
        user = authenticate(request=request)
        if user:
            request.user = user
            get_csrf_token(request)
            return None

        account = Account()
        return account.redirect_login(request)
