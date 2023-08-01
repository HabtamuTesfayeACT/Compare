from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from froala_editor.fields import FroalaField
# from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import datetime
from django.utils.text import slugify
from unidecode import unidecode

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)  # Add this field
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    def count_admin(self):
        Count = CustomUser.objects.filter(is_superuser = True).count()
        return Count
    
    def count_user(self):
        Count = CustomUser.objects.filter(is_user = True).count()
        return Count
    
class Phone(models.Model):
    picture = models.ImageField(upload_to='phones')
    name = models.CharField(max_length=50)
    brand = models.ForeignKey("brand", on_delete=models.CASCADE)
    released_date = models.ForeignKey("anounnced", on_delete=models.CASCADE)
    Phone_model = models.ForeignKey("model", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    
class brand(models.Model):
    brand = models.CharField(max_length=50)
    logo =  models.ImageField(upload_to="brands", null=True)

    def __str__(self):
        return self.brand
    
    def count_phone(self):
        count = Phone.objects.filter(brand__id=self.id).count()
        return count
    

class anounnced(models.Model):
    announced_date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return str(self.announced_date) 
    
class model(models.Model):
    model_name = models.CharField(max_length=50)
    color = models.CharField(max_length=50,null=True)
    body = models.ForeignKey("Body", on_delete=models.CASCADE)
    display = models.ForeignKey("Display", on_delete=models.CASCADE)
    platform = models.ForeignKey("Plattform", on_delete=models.CASCADE)
    memory = models.ForeignKey("Memory", on_delete=models.CASCADE)
    main_camera = models.ForeignKey("Camera", on_delete=models.CASCADE, related_name='main_camera')
    selfi_camera = models.ForeignKey("Camera", on_delete=models.CASCADE,related_name='selfi_camera')
    connectivity = models.ForeignKey("Connectivity", on_delete=models.CASCADE)
    battery = models.ForeignKey("Battery", on_delete=models.CASCADE)
    is_waterproof = models.BooleanField(default=False)

    def __str__(self):
        return self.model_name


class Dimensions(models.Model):
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()

    def __str__(self):
        return str(self.length)+" x "+str(self.width)+" x "+str(self.height) 

class Body(models.Model):
    weight = models.IntegerField()
    bulid = models.CharField(max_length=50)
    Sim_Card = models.CharField(max_length=50)
    dimensions = models.ForeignKey("Dimensions", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.weight) +"g"
    
class Resolution(models.Model):
    width = models.FloatField()
    height = models.FloatField()

    def __str__(self):
        return  str(self.width)+" x "+str(self.height)

class Display(models.Model):
    display_type = models.CharField(max_length=50)
    size_inches = models.FloatField()
    resolution = models.ForeignKey("Resolution",on_delete=models.CASCADE)

    def __str__(self):
        return  self.display_type
    
class Plattform(models.Model):
    operating_sys = models.CharField(max_length=50)
    chipset = models.CharField(max_length=50)
    CPU = models.CharField(max_length=50,null=True)
    GPU = models.CharField(max_length=50,null=True)
    
    def __str__(self):
        return self.operating_sys
    
class Memory(models.Model):
    card_slot = models.CharField(max_length=50)
    RAM =  models.IntegerField(null=True)
    ROM =  models.IntegerField(null=True)


    def __str__(self):
        return str(self.ROM)+" "+str(self.RAM) +" RAM"

class Camera(models.Model):
    module = models.IntegerField(null=True)
    feature = models.CharField(max_length=50)
    video = models.CharField(max_length=50)

    def __str__(self):
        return str(self.module) +" MP"
    
class Connectivity(models.Model):
    wlan = models.CharField(max_length=50)
    bluethooth = models.CharField(max_length=50)
    gps = models.CharField(max_length=50,null=True)
    nfc = models.CharField(max_length=50,null=True)
    infrared = models.CharField(max_length=50,null=True)
    radio = models.CharField(max_length=50,null=True)
    usb = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.wlan
    
class Battery(models.Model):
    size = models.IntegerField()
    battery_type = models.CharField(max_length=50,null=True)
    fast_charging = models.BooleanField()

    def __str__(self):
        return str(self.size)+"mAh"
    
class Store(models.Model):
    store = models.CharField(max_length=50)
    phone = models.ForeignKey("Phone", on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return f"{self.store} - {self.phone.name}"

class Blog_Categories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True,blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            now = datetime.datetime.now()
            self.slug = slugify(unidecode(self.name)) + '-' + now.strftime("%Y-%m-%d")
        super().save(*args, **kwargs)
    
    def count_categories(self):
        return Blog.objects.filter(__type = self.name).count()
    
    def __str__(self) -> str:
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    image = models.ImageField(upload_to='blog/')
    description = models.CharField(max_length=400)
    content = FroalaField()
    type = models.ManyToManyField(Blog_Categories)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            now = datetime.datetime.now()
            self.slug = slugify(unidecode(self.title)) + '-' + now.strftime("%Y-%m-%d")
        super().save(*args, **kwargs)
    
    def count_comment(self):
        return Comment.objects.filter(blog = self.id).count()
    
    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    comment = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self) -> str:
        return self.name
    
class contact(models.Model):
    f_name = models.CharField( max_length=50)
    l_name = models.CharField( max_length=50)
    subject = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return str(self.f_name)+" "+str(self.l_name)


class ComparisonHistory(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    phone_1 = models.CharField(max_length=100)
    phone_2 = models.CharField(max_length=100)
    comparison_result = models.CharField(max_length=100)
    comparison_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_1} vs {self.phone_2} ({self.comparison_date})"
    
class Review(models.Model):
    phone = models.ForeignKey('Phone', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.FloatField()
    text = models.TextField()

    def __str__(self):
        return f"{self.phone.name} - {self.user.username}"