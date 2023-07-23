from django import forms
from .models import brand,Dimensions ,Phone, anounnced, model,Body,Display,Plattform,Memory,Camera,Connectivity,Battery,Resolution,User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import  AdminDateWidget

class Login_Form(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter Your name'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter Your Password'
    }))

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Your First Name'
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Your Last Name'
    }))
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter your Username',
        'autocomplete': 'off' 
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter your Email',
        'autocomplete': 'off'
    }))
    password1 = forms.CharField( max_length=40, label='Password' ,widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter Your Password',
        'autocomplete': 'off'
    }))
    password2 = forms.CharField( max_length=40, label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Confirm Password',
        'autocomplete': 'off'
    }))

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email','password1', 'password2')

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
        widgets = {
            'date_field': AdminDateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(AnnouncedForm, self).__init__(*args, **kwargs)
        self.fields['announced_date'].widget.attrs.update({'class': 'form-control'})
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
