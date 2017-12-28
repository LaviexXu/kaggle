from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label='学号')
    email = forms.EmailField(label='邮箱')
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    name = forms.CharField(label='姓名', max_length=20)
