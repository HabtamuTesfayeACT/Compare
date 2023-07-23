from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import AbstractUser,BaseUserManager

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
    logo =  models.ImageField(upload_to="brands")

    def __str__(self):
        return self.brand
    

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

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    url_to_image = models.URLField()

    def __str__(self):
        return self.title
    

class contact(models.Model):
    f_name = models.CharField( max_length=50)
    l_name = models.CharField( max_length=50)
    email = models.EmailField()
    phone_number = PhoneNumberField()
    message = models.TextField()

    def __str__(self):
        return str(self.f_name)+" "+str(self.l_name)
    
class User(AbstractUser):
    is_active = models.BooleanField('Is_active',default=False)
    is_user = models.BooleanField('Is_user', default=False)
    is_admin = models.BooleanField('Is_admin', default=False)
    photo = models.ImageField(upload_to='user/Photo', null=True, blank=True)

    # EMAIL_FIELD = 'email'
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class ComparisonHistory(models.Model):
    user = models.ForeignKey('user', on_delete=models.CASCADE)
    phone_1 = models.CharField(max_length=100)
    phone_2 = models.CharField(max_length=100)
    comparison_result = models.CharField(max_length=100)
    comparison_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_1} vs {self.phone_2} ({self.comparison_date})"
    
class Review(models.Model):
    product = models.ForeignKey("Phone",on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    author = models.ForeignKey("User",null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.review_text


