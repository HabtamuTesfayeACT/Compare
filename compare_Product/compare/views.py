from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.urls import reverse
from .forms  import BrandForm,PhoneForm,AnnouncedForm,ModelForm,PlatformForm,DisplayForm,BatteryForm,CameraForm,ConnectivityForm,DimensionForm,ResolutionForm,MemoryForm,BodyForm,Login_Form,RegisterForm,ReviewForm
from django.views import View
from .models import brand,Dimensions ,Phone, anounnced, model,Body,Display,Plattform,Review,Memory,Camera,Connectivity,Battery,Resolution,User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from .decorator import login_required,admin_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    phones = Phone.objects.all()
    if request.method == 'POST':
        selected_phones = request.POST.getlist('phones')
        if len(selected_phones) == 2:
            phone1_id = selected_phones[0]
            phone2_id = selected_phones[1]
            url = reverse('phone_comparison', args=[phone1_id, phone2_id])
            return redirect(url)
    else:
        return render(request,"user/index.html", {'phones': phones})

def phone_comparison(request, phone1_id, phone2_id):
    # Retrieve phone data from the database
    phone1 = Phone.objects.get(id=phone1_id)
    phone2 = Phone.objects.get(id=phone2_id)

    phone1_score = 0
    phone2_score = 0

    if phone1.Phone_model.memory.RAM > phone2.Phone_model.memory.RAM:
        phone1_score += 1
    elif phone1.Phone_model.memory.RAM < phone2.Phone_model.memory.RAM:
        phone2_score += 1
    if phone1.Phone_model.main_camera.feature == "Dual-tone LED flash":
        phone1_score += 1
    elif phone2.Phone_model.main_camera.feature == "Dual-tone LED flash":
        phone2_score += 1
    if phone1.Phone_model.is_waterproof:
        phone1_score += 1
    elif phone2.Phone_model.is_waterproof:
        phone2_score += 1
    if phone1.Phone_model.main_camera.module > phone2.Phone_model.main_camera.module:
        phone1_score += 1
    elif phone1.Phone_model.main_camera.module < phone2.Phone_model.main_camera.module:
        phone2_score += 1
    if phone1.Phone_model.display.resolution.width > phone2.Phone_model.display.resolution.width:
        phone1_score += 1
    elif phone1.Phone_model.display.resolution.width < phone2.Phone_model.display.resolution.width:
        phone2_score += 1
    if phone1.Phone_model.memory.ROM > phone2.Phone_model.memory.ROM:
        phone1_score += 1
    elif phone1.Phone_model.memory.ROM < phone2.Phone_model.memory.ROM:
        phone2_score += 1
    if phone1.Phone_model.selfi_camera.module > phone2.Phone_model.selfi_camera.module:
        phone1_score += 1
    elif phone1.Phone_model.selfi_camera.module < phone2.Phone_model.selfi_camera.module:
        phone2_score += 1
    if phone1.Phone_model.body.weight < phone2.Phone_model.body.weight:
        phone1_score += 1
    elif phone1.Phone_model.body.weight > phone2.Phone_model.body.weight:
        phone2_score += 1
    if phone1.Phone_model.battery.size < phone2.Phone_model.battery.size:
        phone1_score += 1
    elif phone1.Phone_model.battery.size > phone2.Phone_model.battery.size:
        phone2_score += 1

    if phone1_score > phone2_score:
        winner = phone1
        difference = phone1_score - phone2_score
    elif phone2_score > phone1_score:
        winner = phone2
        difference = phone2_score - phone1_score
    else:
        winner = "Tie"
        difference = 0

    # Render HTML template with comparison values, winner, and difference
    context = {
        'phone1': phone1,
        'phone2': phone2,
        'score1': phone1_score,
        'score2': phone2_score,
        'winner': winner,
        'difference': difference,
    }
    return render(request, 'user/phone_compare.html', context)


def about(request):
    return render(request,"user/about.html")
def blog(request):
    return render(request,"user/blog.html")
def blog_post(request):
    return render(request,"user/blog-post.html")
def contact(request):
    return render(request,"user/contacts.html")
# def phone_comparison(request,):
#     return render(request, 'user/phone_compare.html')


def review_section(request, phone1_id, phone2_id):
    # Fetch phone data from the database based on the provided IDs
    phone1 = get_object_or_404(Phone, id=phone1_id)
    phone2 = get_object_or_404(Phone, id=phone2_id)

    # Fetch review data from the database based on the fetched phones
    phone1_review = Review.objects.get(phone=phone1)
    phone2_review = Review.objects.get(phone=phone2)

    context = {
        'phone1': phone1,
        'phone2': phone2,
        'phone1_review': phone1_review,
        'phone2_review': phone2_review,
    }
    return render(request, 'review_section.html', context)


def phone_review(request, phone_id):
    phone = Phone.objects.get(pk=phone_id)
    reviews = Review.objects.filter(phone=phone)
    context = {
        'phone': phone,
        'reviews': reviews,
    }
    return render(request, 'phone_review.html', context)

def smart(request):
    displaylist=Phone.objects.all()
    return render(request,"user/smartphones.html",{'smarthpone':displaylist})

def login_view(request):
    user = User.objects.all()
    form = Login_Form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('Admin_home_url')
        else:
            messages.error(request, 'Invalid Password or Email')
    context = {
        'form' : form
    }
    return render(request, 'user/login.html', context)

def register_veiw(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_user = True 
            user.save()
            messages.success(request, 'Your Account has been Successfully Created! Please Login')
            return redirect('login_url')    
    context = {
        'form' : form
    }
    return render(request, 'user/register.html', context)

def smartdetail(request, pk):
    phone = Phone.objects.get(id=pk)
    return render(request, "user/smart-detail.html", {'phone': phone})


# ================================================= admin pages =========================================
# @method_decorator(login_required, name='dispatch')
# @method_decorator(admin_required, name='dispatch')
class AdminIndexView(View):
    def get(self, request):
        return render(request, 'myadmin/index.html')
    
def phoneList(request):
    displaylist=Phone.objects.all()
    return render(request,"myadmin/phone_list.html",{'data':displaylist})
# # ================================================ user managmenet =======================================
# @method_decorator(login_required, name='dispatch')
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'myadmin/user_managment/list_user.html'
    context_object_name = 'users'

# @method_decorator(login_required, name='dispatch')
class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'myadmin/user_managment/create_user.html'
    fields = ['email', 'first_name', 'last_name', 'is_active', 'is_user', 'groups', 'user_permissions']
    success_url = reverse_lazy('user_list')

# @method_decorator(login_required, name='dispatch')
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'myadmin/user_managment/create_user.html.html'
    fields = ['email', 'first_name', 'last_name', 'is_active', 'is_user', 'groups', 'user_permissions']
    success_url = reverse_lazy('user_list')

# @method_decorator(login_required, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('user_list')
    http_method_names = ['post']

class AnnounceDeleteView(DeleteView):
    model = anounnced
    success_url = reverse_lazy('list_announce_url')
    http_method_names = ['post']

class PlatformDeleteView(DeleteView):
    model = Plattform
    success_url = reverse_lazy('list_announce_url')
    http_method_names = ['post']

class ResolutionDeleteView(DeleteView):
    model = Resolution
    success_url = reverse_lazy('list_announce_url')
    http_method_names = ['post']
      
class BatteryDeleteView(DeleteView):
    model = Battery
    success_url = reverse_lazy('list_battery_url')
    http_method_names = ['post']
    
class BodyDeleteView(DeleteView):
    model = Body
    success_url = reverse_lazy('list_body_url')
    http_method_names = ['post']

class BrandDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('list_brand_url')
    http_method_names = ['post']

class CameraDeleteView(DeleteView):
    model = Camera
    success_url = reverse_lazy('list_camera_url')
    http_method_names = ['post']

class ConnectivityDeleteView(DeleteView):
    model = Connectivity
    success_url = reverse_lazy('list_connectivity_url')
    http_method_names = ['post']
    
class DimensionDeleteView(DeleteView):
    model = Dimensions
    success_url = reverse_lazy('list_dimension_url')
    http_method_names = ['post']
    
class DisplayDeleteView(DeleteView):
    model = Display
    success_url = reverse_lazy('list_display_url')
    http_method_names = ['post']
    
class MemoryDeleteView(DeleteView):
    model = Memory
    success_url = reverse_lazy('list_memory_url')
    http_method_names = ['post']

class RsolutionDeleteView(DeleteView):
    model = Resolution
    success_url = reverse_lazy('list_resolution_url')
    http_method_names = ['post']

# ====================================== update =============================================
class Phoneupdate(UpdateView):
    model = Phone
    form_class = PhoneForm
    template_name = 'myadmin/add-phone.html'
    success_url = reverse_lazy('update_phone_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_page'] = True  # Set to True if the user is on the update page
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Phone updated successfully.')
        return super().form_valid(form)
    
class Modelupdate(UpdateView):
    model = model  # 'Model' should be replaced with the name of your model
    form_class = ModelForm
    template_name = 'myadmin/add-model.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_page'] = True
        return context

    def get_success_url(self):
        return reverse('model_update', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Phone updated successfully.')
        return super().form_valid(form)

    
class resolutionupdate(UpdateView):
    model = Resolution
    form_class = ResolutionForm
    template_name = 'myadmin/add_resolution.html'
    success_url = reverse_lazy('Admin_resolution_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_page'] = True  # Set to True if the user is on the update page
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Phone updated successfully.')
        return super().form_valid(form)
    
class platformupdate(UpdateView):
    model = Plattform
    form_class = PlatformForm
    template_name = 'myadmin/add_platform.html'
    success_url = reverse_lazy('Admin_platform_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_page'] = True  # Set to True if the user is on the update page
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Phone updated successfully.')
        return super().form_valid(form)
    
class memoryupdate(UpdateView):
    model = Memory
    form_class = MemoryForm
    template_name = 'myadmin/add_memory.html'
    success_url = reverse_lazy('Admin_memory_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_page'] = True  # Set to True if the user is on the update page
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Phone updated successfully.')
        return super().form_valid(form)
    
class Displayupdate(UpdateView):
    model = Display
    form_class = DisplayForm
    template_name = 'myadmin/add_display.html'
    success_url = reverse_lazy('Admin_display_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_page'] = True  # Set to True if the user is on the update page
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Phone updated successfully.')
        return super().form_valid(form)
    
class Dimensionupdate(UpdateView):
    model = Dimensions
    form_class = DimensionForm
    template_name = 'myadmin/add_dimension.html'
    success_url = reverse_lazy('Admin_dimension_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_page'] = True  # Set to True if the user is on the update page
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Phone updated successfully.')
        return super().form_valid(form)

class connectivityUpdate(UpdateView):
    model = Connectivity
    form_class = ConnectivityForm
    template_name = 'myadmin/add_connectivity.html'
    success_url = reverse_lazy('Admin_connectivty_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_page'] = True  # Set to True if the user is on the update page
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Phone updated successfully.')
        return super().form_valid(form)

class cameraupdate(UpdateView):
    model = Camera
    form_class = CameraForm
    template_name = 'myadmin/add_camera.html'
    success_url = reverse_lazy('Admin_camera_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_page'] = True  # Set to True if the user is on the update page
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Phone updated successfully.')
        return super().form_valid(form)

class brandupdate(UpdateView):
    model = brand
    form_class = BrandForm
    template_name = 'myadmin/add_brand.html'
    success_url = reverse_lazy('brand_update')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_page'] = True  # Set to True if the user is on the update page
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Phone updated successfully.')
        return super().form_valid(form)

class bodyupdate(UpdateView):
    model = Body
    form_class = BodyForm
    template_name = 'myadmin/add_body.html'
    success_url = reverse_lazy('Admin_body_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_page'] = True  # Set to True if the user is on the update page
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Phone updated successfully.')
        return super().form_valid(form)

class batteryupdate(UpdateView):
    model = Battery
    form_class = BatteryForm
    template_name = 'myadmin/add_battery.html'
    success_url = reverse_lazy('Admin_battery_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_page'] = True  # Set to True if the user is on the update page
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Phone updated successfully.')
        return super().form_valid(form)
    
class announceupdate(UpdateView):
    model = anounnced
    form_class = AnnouncedForm
    template_name = 'myadmin/add_announced.html'
    success_url = reverse_lazy('Admin_announce_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_page'] = True  # Set to True if the user is on the update page
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Phone updated successfully.')
        return super().form_valid(form)

# ============================================== model managment =========================================
class AddModelView(View):
    def get(self, request):
        form = ModelForm()
        context = {'form': form, 'is_add_page': True}
        return render(request, 'myadmin/add-model.html', context)
    
    
    def post(self, request):
        form = ModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Admin_model_url')
        return render(request, 'myadmin/add-model.html', {'form': form})    
    
class ModelListView(View):
    def get(self, request):
        models = model.objects.all()
        return render(request, 'myadmin/model_list.html', {'models': models})

class ModelUpdateView(View):
    def get(self, request, pk):
        model = get_object_or_404(model, pk=pk)
        form = ModelForm(instance=model)
        return render(request, 'myadmin/edit_model.html', {'form': form})

    def post(self, request, pk):
        model = get_object_or_404(model, pk=pk)
        form = ModelForm(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect('model_list')
        return render(request, 'myadmin/edit_model.html', {'form': form})

class ModelDeleteView(View):
    def post(self, request, pk):
        model = get_object_or_404(model, pk=pk)
        model.delete()
        return redirect('model_list')
# ============================================== End of model =============================================
class AddPhoneView(View):
    def get(self, request):
        form = PhoneForm()
        context = {'form': form, 'is_add_page': True}
        return render(request, 'myadmin/add-phone.html',context)
    
    def post(self, request):
        form = PhoneForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Admin_phone_url')
        return render(request, 'myadmin/add-phone.html', {'form': form,})
        
class AddBrandView(View):
    def get(self, request):
        form = BrandForm()
        context = {'form': form, 'is_add_page': True}
        return render(request, 'myadmin/add_brand.html',context)
    def post(self, request):
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Admin_brand_url')
        return render(request, 'myadmin/add_brand.html', {'form': form})
    
class AddDisplayView(View):
    def get(self, request):
        form = DisplayForm()
        context = {'form': form, 'is_add_page': True}
        return render(request, 'myadmin/add_display.html', context)

    def post(self, request):
        form = DisplayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Admin_display_url')
        return render(request, 'myadmin/add_display.html', {'form': form})
    
class AddCameraView(View):
    def get(self, request):
        form = CameraForm()
        context = {'form': form, 'is_add_page': True}
        return render(request, 'myadmin/add_camera.html', context)
    
    def post(self, request):
        form = CameraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Admin_camera_url')
        return render(request, 'myadmin/add_camera.html', {'form': form})

class AddBodyView(View):
    def get(self, request):
        form = BodyForm()
        context = {'form': form, 'is_add_page': True}
        return render(request, 'myadmin/add_body.html', context)
    
    def post(self, request):
        form = BodyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Admin_body_url')
        return render(request, 'myadmin/add_body.html', {'form': form})

class AddAnnouncedView(View):
    def get(self, request):
        form = AnnouncedForm()
        context = {'form': form, 'is_add_page': True}
        return render(request, 'myadmin/add_announced.html', context)

    def post(self, request):
        form = AnnouncedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Admin_announce_url')
        return render(request, 'myadmin/add_announced.html', {'form': form})

class AddDimensionView(View):
    def get(self, request):
        form = DimensionForm()
        context = {'form': form, 'is_add_page': True}
        return render(request, 'myadmin/add_dimension.html', context)

    def post(self, request):
        form = DimensionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Admin_dimension_url')
        return render(request, 'myadmin/add_dimension.html', {'form': form})
    
class AddPlatformView(View):
    def get(self, request):
        form = PlatformForm()
        context = {'form': form, 'is_add_page': True}
        return render(request, 'myadmin/add_platform.html', context)

    def post(self, request):
        form = PlatformForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Admin_platform_url')
        return render(request, 'myadmin/add_platform.html', {'form': form})
    
class AddResolutionView(View):
    def get(self, request):
        form = ResolutionForm()
        context = {'form': form, 'is_add_page': True}
        return render(request, 'myadmin/add_resolution.html',context)

    def post(self, request):
        form = ResolutionForm(request.POST)
        if form.is_valid():
            resolution = form.save()
            data = {'id': resolution.id, 'name': f'{resolution.width}x{resolution.height}'}
            return JsonResponse(data)
        else:
            return JsonResponse(form.errors, status=400)
            return redirect('Admin_resolution_url')
        return render(request, 'myadmin/add_resolution.html', {'form': form})
    
class AddMemoryView(View):
    def get(self, request):
        form = MemoryForm()
        context = {'form': form, 'is_add_page': True}
        return render(request, 'myadmin/add_memory.html',context)

    def post(self, request):
        form = MemoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Admin_memory_url')
        return render(request, 'myadmin/add_memory.html', {'form': form})
    
class AddConnectView(View):
    def get(self, request):
        form = ConnectivityForm()
        context = {'form': form, 'is_add_page': True}
        return render(request, 'myadmin/add_connectivity.html',context)

    def post(self, request):
        form = ConnectivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Admin_connectivty_url')
        return render(request, 'myadmin/add_connectivity.html', {'form': form})
     
class AddbatteryView(View):
    def get(self, request):
        form = BatteryForm()
        context = {'form': form, 'is_add_page': True}
        return render(request, 'myadmin/add_battery.html',context)
    
    def post(self, request):
        form = BatteryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Admin_battery_url')
        return render(request, 'myadmin/add_battery.html', {'form': form})
    
# ============================================== listing =================================================
class BrandListView(ListView):
    model = brand
    template_name = 'myadmin/phone_components/brand.html'
    context_object_name = 'brands'

class AnnouncedListView(ListView):
    model = anounnced
    template_name = 'myadmin/phone_components/announed.html'
    context_object_name = 'announceds'

class BodyListView(ListView):
    model = Body
    template_name = 'myadmin/phone_components/bodys.html'
    context_object_name = 'bodies'

class DisplayListView(ListView):
    model = Display
    template_name = 'myadmin/phone_components/display.html'
    context_object_name = 'displays'

class PlatformListView(ListView):
    model = Plattform
    template_name = 'myadmin/phone_components/platform.html'
    context_object_name = 'platforms'

class DimensionListView(ListView):
    model = Dimensions
    template_name = 'myadmin/phone_components/dimension.html'
    context_object_name = 'dimensions'
    
class ResolutionListView(ListView):
    model = Resolution
    template_name = 'myadmin/phone_components/resolution.html'
    context_object_name = 'resolutions'

class MemoryListView(ListView):
    model = Memory
    template_name = 'myadmin/phone_components/memory.html'
    context_object_name = 'memories'

class CameraListView(ListView):
    model = Camera
    template_name = 'myadmin/phone_components/camera.html'
    context_object_name = 'cameras'

class ConnectivityListView(ListView):
    model = Connectivity
    template_name = 'myadmin/phone_components/connectivity.html'
    context_object_name = 'connectivities'

class BatteryListView(ListView):
    model = Battery
    template_name = 'myadmin/phone_components/battery.html'
    context_object_name = 'batteries'

