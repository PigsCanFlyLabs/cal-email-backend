from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

import google_auth_oauthlib
from googleapiclient.discovery import build

from cal_sync_magic.models import *


def get_redirect_uri(request):
    return str(request.build_absolute_uri(reverse("google-oauth-callback")))

class GoogleAuthView(LoginRequiredMixin, View):
    def get(self, request):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            settings.GOOGLE_CLIENT_SECRETS_FILE, scopes=scopes)
        redirect_uri = get_redirect_uri(request)
        print(f"Redirect uri is {redirect_uri}")
        flow.redirect_uri = redirect_uri
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')
        request.session['google_auth_state'] = state
        # Redirect the user to the authorization url
        return redirect(authorization_url)

class GoogleCallBackView(LoginRequiredMixin, View):
    def get(self, request):
        state = request.session['google_auth_state']
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            settings.GOOGLE_CLIENT_SECRETS_FILE, scopes=scopes, state=state)
        redirect_uri = get_redirect_uri(request)
        flow.redirect_uri = redirect_uri
        authorization_response = (redirect_uri + "?"
                                  + request.META['QUERY_STRING'])
        print(f"Auth response is {authorization_response}")
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        user_info_service = build('oauth2', 'v2', credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()
        google_user_email = user_info['email']
        account = GoogleAccount.objects.update_or_create(
            user = request.user,
            google_user_email=google_user_email,
            defaults={
                "credential_expiry": credentials.expiry,
                "credentials": credentials.to_json(),
                "last_refreshed": datetime.now()})
        return redirect(reverse("update-user-calendars"))

class UpdateUserCalendars(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        for account in GoogleAccount.objects.filter(user = request.user):
            account.refresh_calendars()
        return redirect(reverse("sync-config"))


class ConfigureSyncs(LoginRequiredMixin, View):
    def get(self, request):
        google_accounts = GoogleAccount.objects.filter(user = request.user)
        calendars = UserCalendar.objects.filter(user = request.user)
        syncs = SyncConfigs.objects.filter(user = request.user)
        return render(request, 'configure_sync.html', context={
            'title': "Configure calendar syncing",
            'google_accounts': google_accounts,
            'calendars': calendars,
            'syncs': syncs
            })
