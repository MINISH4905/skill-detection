from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']



from .models import Domain


class DomainSelectionForm(forms.Form):
    domains = forms.ModelMultipleChoiceField(
        queryset=Domain.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

class ActivityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        profile = user.userprofile
        self.fields['domain'].queryset = profile.selected_domains.all()