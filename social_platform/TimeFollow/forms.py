from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Row, Column, Layout
from .models import Post, CustomUser
from phonenumber_field.formfields import PhoneNumberField

######## New User Form ########
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone_num = PhoneNumberField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_num', 'password1', 'password2', 'first_name', 'last_name']
    
    def clean_phone_num(self):
        phone_no = self.cleaned_data.get('phone_num', None)
        try:
            num = phone_no.raw_input.replace(" ","")
            int(num)
        except:
            raise forms.ValidationError('Please enter a valid phone number e.g. "0123456789".')
        
        return phone_no

######## New Post Form ########
class NewPost(forms.ModelForm):
    postContent = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows':4, 'style':'resize: None'}
            ),
        max_length=200, label="Post content")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-newPost'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'createpost'
        self.helper.add_input(Submit('create post','Create Post',))

    class Meta:
        model = Post
        fields = [ "postContent"]

######## Edit Profile Form ########
class EditProfile(forms.ModelForm):
    phone_num = PhoneNumberField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        self.helper = FormHelper()
        self.helper.form_id = 'id-newPost'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'profile'
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-12 mb-0')
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0')
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('phone_num', css_class='form-group col-md-6 mb-0')
            ),
            Submit('Save changes', 'Save Changes',)
        )

    class Meta:
        model = CustomUser
        exclude = ["id", "password", "groups", "user_permissions", "is_superuser", "is_staff", "is_active", "last_login", "date_joined"]

    def clean_phone_num(self):
        phone_no = self.cleaned_data.get('phone_num', None)
        try:
            num = phone_no.raw_input.replace(" ","")
            int(num)
        except:
            raise forms.ValidationError('Please enter a valid phone number e.g. "0123456789".')
        
        return phone_no
    
class changePassword(PasswordChangeForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id-passwordChange'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'passwordchange'
        self.helper.add_input(Submit('change password','Change Password',))