from django import forms

from chat_app.models import Chat, User


class LoginForm(forms.Form):
    """
    User login form
    """
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class CreateChatForm(forms.ModelForm):
    name = forms.CharField(required=True)
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select users to add"
    )

    class Meta:
        model = Chat
        fields = ('name', 'users')
