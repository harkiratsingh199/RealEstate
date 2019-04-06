from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import TemplateView, View, RedirectView
from django.contrib.auth import login, logout, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect



from Rehma11bRealEstate import settings


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'adminAccountTemplates/admin_dashboard.html'
#
# class sign_in(View):
#     template_name = 'pages/sign_in.html'
#
#     def get(self, request):
#         redirect_to = request.GET['next'] if 'next' in request.GET else '/'
#         return render(request, self.template_name, {'sign_in': sign_in})
#
#     def post(self, request):
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             # Redirect to a success page.
#             redirect_to = request.POST['redirect_to']
#             return redirect(redirect_to)
#         else:
#             # Return an 'invalid login' error message.
#             return render(request, self.template_name, {'error_message': 'Invalid Login'})


class AdminLoginView(View):
    template_name = 'adminAccountTemplates/login.html'

    def get(self, request):
        redirect_to = request.GET['next'] if 'next' in request.GET else '/'
        return render(request, self.template_name, {'redirect_to': redirect_to})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            redirect_to = request.POST['redirect_to']
            return redirect(redirect_to)
        else:
            # Return an 'invalid login' error message.
            return render(request, self.template_name, {'error_message': 'Invalid Login'})


class LogoutView(RedirectView):

    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


