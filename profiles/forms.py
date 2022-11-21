from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import Profile, ProfileImage
from dating_app import settings

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

# This will definitely work
class MyUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'maxlength':'12', 'class': 'form-control'}))
    password1 = forms.CharField(label="Enter Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].required = True

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        
    def cleaned_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'Email address has been used previously. Please choose another')
    
        # Add cleaned username
    
        return email
    
    def cleaned_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if not password1 or password2:
            raise ValidationError("Password fields must be filled in")
            
        if password1 != password2:
            raise ValidationError("Passwords do not match. Please try again.")
            
        return password2    
        
class EditProfileForm(UserChangeForm):
    password = None
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    # Get rid of password help text
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(EditProfileForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['confirm_password', 'username']:
            self.fields[fieldname].help_text = None

    def clean_confirm_password(self):
        password = self.cleaned_data['confirm_password']
        if not self.user.check_password(password):
            raise forms.ValidationError("Incorrect Password Entered")
        return password
        
    
    class Meta:
        model = User
        fields = ('email', 'username')

        
class ProfileForm(forms.ModelForm):
    LOOKING_FOR = (
      ('MALE', 'Men'),
      ('FEMALE', 'Women'),
      ('BOTH', 'Both'),
    )
    RELATIONSHIP_STATUS = (
      ('SINGLE', 'Single'),
      ('IN_RELATIONSHIP', 'In relationship'),
    )
    about = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'maxlength': '200'}), required=True)
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    # gender = forms.ChoiceField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    # relationship_status = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    looking_for = forms.ChoiceField(choices=LOOKING_FOR, initial='', widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    relationship_status = forms.ChoiceField(choices=RELATIONSHIP_STATUS, initial='', widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    class Meta:
        model = Profile
        fields = ( 'about', 'relationship_status', 'looking_for',  'location') 


class PersonalInformationForm(forms.Form):
    GENDER = (
      ("MALE", "Male"),
      ("FEMALE", "Female"),
      ("OTHER", "Other")
    )
    gender = forms.ChoiceField(choices=GENDER, initial='', widget=forms.Select(attrs={'class': 'form-control'}), required=True)


# class AccountManagementForm(forms.Form):
#     old_password = forms.

# class MessagesForm(forms.ModelForm):
#     # message_content = forms.CharField(widget=forms.TextInput)
    
#     class Meta:
#         model = Messages
#         fields = ('message_content', )
