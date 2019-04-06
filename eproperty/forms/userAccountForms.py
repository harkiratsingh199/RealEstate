
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import Profile
from django.forms import Form, ModelForm, TextInput, EmailInput, DateInput, DateField, PasswordInput, \
    ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from eproperty.models.userAccountModels import User,Role, Permission, UserProfile, UserRole, RolePermission
from django.utils.timezone import now

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']



class UserCreateForm(ModelForm):
    account_expiry_date = DateField(widget=DateInput(attrs={'class': 'input date-input'}), required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'Email Address'}),
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'User Name'}),
            'password': PasswordInput(attrs={'class': 'input'})
        }

    def is_valid(self):

        # run parent validation first
        valid = super(UserCreateForm, self).is_valid()
        if not valid:
            return valid

        # check if username or email already exists
        try:
            user = User.objects.get(email=self.cleaned_data['email'])

            if user is not None:
                self.add_error('email', 'Email Already Exists!')
                return False

        # no user with this username or email address
        except User.DoesNotExist:
            pass

        return True

    def save(self, commit=True):
        user = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'],
                                        self.cleaned_data['password'])
        user.last_name = self.cleaned_data['last_name']
        user.first_name = self.cleaned_data['first_name']
        user.save()
        profile = UserProfile(user=user, account_expiry_date=self.cleaned_data['account_expiry_date'])
        profile.save()
        return user




class UserUpdateForm(ModelForm):
    account_expiry_date = DateField(widget=DateInput(attrs={'class': 'input date-input'}), required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'Email Address'}),
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'User Name'})
        }

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit)
        profile = UserProfile.objects.get(user=user)
        expiry = self.cleaned_data['account_expiry_date']
        if profile.account_expiry_date != expiry:
            profile.account_expiry_date = expiry
            profile.save()
        return user


class AssignRoleForm(Form):
    roles = ModelMultipleChoiceField(widget=CheckboxSelectMultiple(), queryset=Role.objects.all())

    def save(self, user, selected_roles):
        user_roles = UserRole.objects.filter(user=user)
        for role in user_roles:
            if role.role_id not in selected_roles:
                role.delete()

        for role_id in selected_roles:
            if role_id not in [a.role_id for a in user_roles]:
                ur = UserRole(user=user, role_id=role_id)
                ur.save()


class ManagePermissionForm(Form):
    features = ModelMultipleChoiceField(widget=CheckboxSelectMultiple(), queryset=Permission.objects.all())

    def save(self, role, selected_features):
        role_permissions = RolePermission.objects.filter(role=role)
        for permission in role_permissions:
            if permission.permission_id not in selected_features:
                permission.delete()

        for permission_id in selected_features:
            if permission_id not in [a.permission_id for a in role_permissions]:
                ur = RolePermission(role=role, permission_id=permission_id)
                ur.save()


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['name']


class FeatureForm(ModelForm):
    class Meta:
        model = Permission
        fields = ['sysFeature']
