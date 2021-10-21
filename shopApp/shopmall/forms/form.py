from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=12, min_length=6, required=True, error_messages={'required':'帳號不得為空', 'invalid':'帳號格式不符'}, widget=forms.TextInput(attrs={'class':'className'}), help_text='help')
    passwd = forms.CharField(max_length=16, min_length=8, required=True, error_messages={'required': '密碼不得為空', 'invalid': '密碼格式不符'}, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=12, min_length=6, required=True, error_messages={'required':'帳號不得為空', 'invalid':'帳號格式不符'}, widget=forms.TextInput(attrs={'class':'className'}), help_text='help')
    passwd = forms.CharField(max_length=16, min_length=8, required=True, error_messages={'required': '密碼不得為空', 'invalid': '密碼格式不符'}, widget=forms.PasswordInput)