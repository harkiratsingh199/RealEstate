from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from eproperty.models.userAccountModels import UserProfile, User, UserRole
from eproperty.forms.userAccountForms import UserCreateForm, UserUpdateForm, AssignRoleForm
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView


class UserList(ListView):
    model = UserProfile
    template_name = 'manage_users/list.html'
    context_object_name = 'users'
    # queryset = User.objects.filter(is_staff=False)


class UserCreate(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'manage_users/user.html'
    success_url = '/users'

    def get_success_url(self):
        return self.success_url


class UserUpdate(UpdateView):
    model = UserProfile
    form_class = UserUpdateForm
    template_name = 'manage_users/user.html'
    success_url = '/users'

    # def get_form(self, form_class=form_class):
    #     form = super(UserUpdate, self).get_form(form_class)
    #     username = form.instance.username
    #     profile = UserProfile.objects.get(user__username=username)
    #     form.fields['account_expiry_date'].initial = profile.account_expiry_date
    #     return form


class UserDelete(DeleteView):
    model = UserProfile
    template_name = 'manage_users/delete.html'
    success_url = '/users'


# class UserUpdate(UpdateView):
#     model = User
#     form_class = UserUpdateForm
#     template_name = 'manage_users/user.html'
#     success_url = '/system-admin/users'
#
#     def get_form(self, form_class=form_class):
#         form = super(UserUpdate, self).get_form(form_class)
#         username = form.instance.username
#         profile = UserProfile.objects.get(user__username=username)
#         form.fields['account_expiry_date'].initial = profile.account_expiry_date
#         return form


# class UserDelete(DeleteView):
#     model = UserProfile
#     template_name = 'manage_users/delete.html'
#     success_url = '/system-admin/users'

class UserEnable(FormView):
    template_name = 'manage_users/enable.html'
    success_url = '/users'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        text = 'disable' if user.is_active else 'enable'
        return render(request, self.template_name, {'user': user, 'text': text})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        user.is_active = not user.is_active
        user.save()
        return HttpResponseRedirect(self.success_url)


class AssignRole(FormView):
    template_name = 'manage_users/assign_role.html'
    success_url = '/users'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        user_roles = UserRole.objects.filter(user=user)
        form = AssignRoleForm(initial={'roles': [a.role_id for a in user_roles]}) if any(user_roles) else AssignRoleForm()
        return render(request, self.template_name, {'user': user, 'form': form})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        form = AssignRoleForm(request.POST)
        selected_roles = request.POST.getlist('roles')
        form.save(user, selected_roles)
        return HttpResponseRedirect(self.success_url)
