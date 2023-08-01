# forms.py
from django import forms
from .models import brand,Dimensions ,Phone, anounnced, model,Body,Display,Plattform,Memory,Camera,Connectivity,Review,Battery,Resolution,CustomUser,Comment,contact
from django.contrib.admin.widgets import  AdminDateWidget
from django.forms.widgets import DateInput
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name']  # Add more fields as needed


class AdminCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [ 'first_name', 'last_name','email', 'password', 'is_user', 'is_superuser','is_active']

    def __init__(self, *args, **kwargs):
        super(AdminCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

class BrandForm(forms.ModelForm):
    class Meta:
        model = brand
        fields = ['brand', 'logo']

    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        self.fields['brand'].widget.attrs.update({'class': 'form-control'})
        self.fields['logo'].widget.attrs.update({'class': 'file-upload__label'})

class AnnouncedForm(forms.ModelForm):
    class Meta:
        model = anounnced
        fields = ['announced_date', 'status']

    def __init__(self, *args, **kwargs):
        super(AnnouncedForm, self).__init__(*args, **kwargs)
        self.fields['announced_date'].widget =DateInput(attrs={'type': 'date', 'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})

class DimensionForm(forms.ModelForm):
    class Meta:
        model = Dimensions
        fields = ['length', 'width','height']

    def __init__(self, *args, **kwargs):
        super(DimensionForm, self).__init__(*args, **kwargs)
        self.fields['length'].widget.attrs.update({'class': 'form-control'})
        self.fields['width'].widget.attrs.update({'class': 'form-control'})
        self.fields['height'].widget.attrs.update({'class': 'form-control'})

class BodyForm(forms.ModelForm):
    class Meta:
        model = Body
        fields = ['weight', 'bulid', 'Sim_Card', 'dimensions']

    dimensions = forms.ModelChoiceField(queryset=Dimensions.objects.all(), widget=forms.Select(attrs={'class': 'form-control p-1'}))

    def __init__(self, *args, **kwargs):
        super(BodyForm, self).__init__(*args, **kwargs)
        self.fields['weight'].widget.attrs.update({'class': 'form-control'})
        self.fields['bulid'].widget.attrs.update({'class': 'form-control'})
        self.fields['Sim_Card'].widget.attrs.update({'class': 'form-control'})

class ResolutionForm(forms.ModelForm):
    class Meta:
        model = Resolution
        fields = ['width','height']

    def __init__(self, *args, **kwargs):
            super(ResolutionForm, self).__init__(*args, **kwargs)
            self.fields['width'].widget.attrs.update({'class': 'form-control'})
            self.fields['height'].widget.attrs.update({'class': 'form-control'})

class DisplayForm(forms.ModelForm):
    class Meta:
        model = Display
        fields = ['display_type','size_inches','resolution']

    resolution = forms.ModelChoiceField(queryset=Resolution.objects.all(), widget=forms.Select(attrs={'class': 'form-control p-1'}))

    def __init__(self, *args, **kwargs):
        super(DisplayForm, self).__init__(*args, **kwargs)
        self.fields['display_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['size_inches'].widget.attrs.update({'class': 'form-control'})

class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ['card_slot','RAM','ROM']

    def __init__(self, *args, **kwargs):
        super(MemoryForm, self).__init__(*args, **kwargs)
        self.fields['card_slot'].widget.attrs.update({'class': 'form-control'})
        self.fields['RAM'].widget.attrs.update({'class': 'form-control'})
        self.fields['ROM'].widget.attrs.update({'class': 'form-control'})


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
    

class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ['module','feature','video']

    def __init__(self, *args, **kwargs):
        super(CameraForm, self).__init__(*args, **kwargs)
        self.fields['module'].widget.attrs.update({'class': 'form-control'})
        self.fields['feature'].widget.attrs.update({'class': 'form-control'})
        self.fields['video'].widget.attrs.update({'class': 'form-control'})

class ConnectivityForm(forms.ModelForm):
    class Meta:
        model = Connectivity
        fields = ['wlan','bluethooth','gps',"nfc",'infrared','radio','usb']

    def __init__(self, *args, **kwargs):
            super(ConnectivityForm, self).__init__(*args, **kwargs)
            self.fields['wlan'].widget.attrs.update({'class': 'form-control'})
            self.fields['bluethooth'].widget.attrs.update({'class': 'form-control'})
            self.fields['gps'].widget.attrs.update({'class': 'form-control'})
            self.fields['nfc'].widget.attrs.update({'class': 'form-control'})
            self.fields['infrared'].widget.attrs.update({'class': 'form-control'})
            self.fields['radio'].widget.attrs.update({'class': 'form-control'})
            self.fields['usb'].widget.attrs.update({'class': 'form-control'})

class BatteryForm(forms.ModelForm):
    class Meta:
        model = Battery
        fields = ['size','battery_type','fast_charging']

    def __init__(self, *args, **kwargs):
            super(BatteryForm, self).__init__(*args, **kwargs)
            self.fields['size'].widget.attrs.update({'class': 'form-control'})
            self.fields['battery_type'].widget.attrs.update({'class': 'form-control'})
            self.fields['fast_charging'].widget.attrs.update({'class': 'form-control'})

class PlatformForm(forms.ModelForm):
    class Meta:
        model = Plattform
        fields = ['operating_sys', 'chipset','CPU','GPU']

    def __init__(self, *args, **kwargs):
            super(PlatformForm, self).__init__(*args, **kwargs)
            self.fields['operating_sys'].widget.attrs.update({'class': 'form-control'})
            self.fields['chipset'].widget.attrs.update({'class': 'form-control'})
            self.fields['CPU'].widget.attrs.update({'class': 'form-control'})
            self.fields['GPU'].widget.attrs.update({'class': 'form-control'})

class ModelForm(forms.ModelForm):
    class Meta:
        model = model
        fields = ('model_name', 'body', 'display', 'platform', 'memory', 'main_camera', 'selfi_camera', 'connectivity', 'battery','is_waterproof')
    
    body = forms.ModelChoiceField(queryset=Body.objects.all(), widget=forms.Select(attrs={'class': 'form-control  p-1'}))
    display = forms.ModelChoiceField(queryset=Display.objects.all(), widget=forms.Select(attrs={'class': 'form-control p-1'}))
    platform = forms.ModelChoiceField(queryset=Plattform.objects.all(), widget=forms.Select(attrs={'class': 'form-control p-1'}))
    memory = forms.ModelChoiceField(queryset=Memory.objects.all(), widget=forms.Select(attrs={'class': 'form-control p-1'}))
    main_camera = forms.ModelChoiceField(queryset=Camera.objects.all(), widget=forms.Select(attrs={'class': 'form-control p-1'}))
    selfi_camera = forms.ModelChoiceField(queryset=Camera.objects.all(), widget=forms.Select(attrs={'class': 'form-control p-1'}))
    connectivity = forms.ModelChoiceField(queryset=Connectivity.objects.all(), widget=forms.Select(attrs={'class': 'form-control p-1'}))
    battery = forms.ModelChoiceField(queryset=Battery.objects.all(), widget=forms.Select(attrs={'class': 'form-control p-1'}))

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['model_name'].widget.attrs.update({'class': 'form-control'})

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['picture', 'name', 'brand', 'released_date', 'Phone_model']
        
        brand = forms.ModelChoiceField(queryset=brand.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
        released_date = forms.ModelChoiceField(queryset=anounnced.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
        Phone_model = forms.ModelChoiceField(queryset=model.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(PhoneForm, self).__init__(*args, **kwargs)
        self.fields['picture'].widget.attrs.update({'class': 'file-upload__label'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['Phone_model'].widget.attrs.update({'class': 'form-control p-1'})
        self.fields['brand'].widget.attrs.update({'class': 'form-control p-1'})
        self.fields['released_date'].widget.attrs.update({'class': 'form-control p-1'})

class CommentForm(forms.ModelForm):
    name = forms.CharField(max_length=40, error_messages={'required' : 'Can not be empty'})
    email = forms.EmailField(widget=forms.TextInput(), error_messages={'required' : 'Can not be empty'})
    comment = forms.CharField(widget=forms.TextInput(), error_messages={'required': 'Can not be empty'})
    
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise forms.ValidationError(' Enter a valid name.')
        return name
    
class ContactForm(forms.ModelForm):
    f_name = forms.CharField(max_length=40, error_messages={'required' : 'Can not be empty'})
    l_name = forms.CharField(max_length=40, error_messages={'required' : 'Can not be empty'})
    email = forms.EmailField(error_messages={'required' : 'Can not be empty'})
    subject = forms.CharField(error_messages={'required' : 'Can not be empty'})
    message = forms.CharField(widget=forms.TextInput, error_messages={'required' : 'Can not be empty'})

    class Meta:
        model = contact
        fields = '__all__'
    
    def clean_name(self):
     name = self.cleaned_data['name']
     if len(name) < 2:
         raise forms.ValidationError(' Enter a valid name.')
     return name
