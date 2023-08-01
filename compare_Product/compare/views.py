from datetime import timezone
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.urls import reverse
from django.core.paginator import Paginator
from .forms  import LoginForm, RegistrationForm,AdminCreationForm,BrandForm,PhoneForm,AnnouncedForm,ModelForm,PlatformForm,DisplayForm,BatteryForm,CameraForm,ConnectivityForm,DimensionForm,ResolutionForm,MemoryForm,BodyForm,ReviewForm,CommentForm
from django.views import View
from .models import brand,Dimensions ,Phone, anounnced, model,Body,Display,Plattform,Review,Memory,Camera,Connectivity,Battery,Resolution,CustomUser,Blog, Comment,contact,ComparisonHistory,Blog_Categories
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .decorator import login_required,admin_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('Admin_home_url')
            elif user is not None and user.is_user:
                login(request, user)
                return redirect('home_url')
            else:
                messages.error(request, 'Invalid Password or Email')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create user instance without saving to the database yet
            user.is_user = True  # Set is_candidate to True
            form.save()
            messages.success(request, 'User registration successful!')
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'user/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_url')

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

    comparison_data = {
        'phone1': {
            'name': phone1.name,
            'advantages': [],
            'disadvantages': [],
        },
        'phone2': {
            'name': phone2.name,
            'advantages': [],
            'disadvantages': [],
        },
    }

    # Weight Comparison
    if phone1.Phone_model.body.weight < phone2.Phone_model.body.weight:
        phone1_score += 1
        comparison_data['phone1']['advantages'].append('Lighter Weight: ' + str(phone1.Phone_model.body.weight) + 'g vs ' + str(phone2.Phone_model.body.weight) + 'g. We believe a lighter phone is better for handling.')
        comparison_data['phone2']['disadvantages'].append('Heavier Weight: ' + str(phone2.Phone_model.body.weight) + 'g vs ' + str(phone1.Phone_model.body.weight) + 'g. A heavier phone might be less comfortable for long term use.')
    elif phone1.Phone_model.body.weight > phone2.Phone_model.body.weight:
        phone2_score += 1
        comparison_data['phone2']['advantages'].append('Lighter Weight: ' + str(phone2.Phone_model.body.weight) + 'g vs ' + str(phone1.Phone_model.body.weight) + 'g. We believe a lighter phone is better for handling.')
        comparison_data['phone1']['disadvantages'].append('Heavier Weight: ' + str(phone1.Phone_model.body.weight) + 'g vs ' + str(phone2.Phone_model.body.weight) + 'g. A heavier phone might be less comfortable for long term use.')

    # RAM Comparison
    if phone1.Phone_model.memory.RAM > phone2.Phone_model.memory.RAM:
        phone1_score += 1
        comparison_data['phone1']['advantages'].append('More RAM: ' + str(phone1.Phone_model.memory.RAM) + 'GB vs ' + str(phone2.Phone_model.memory.RAM) + 'GB. More RAM allows for better multitasking and smoother performance.')
        comparison_data['phone2']['disadvantages'].append('Less RAM: ' + str(phone2.Phone_model.memory.RAM) + 'GB vs ' + str(phone1.Phone_model.memory.RAM) + 'GB. Less RAM might impact multitasking and performance.')
    elif phone1.Phone_model.memory.RAM < phone2.Phone_model.memory.RAM:
        phone2_score += 1
        comparison_data['phone2']['advantages'].append('More RAM: ' + str(phone2.Phone_model.memory.RAM) + 'GB vs ' + str(phone1.Phone_model.memory.RAM) + 'GB. More RAM allows for better multitasking and smoother performance.')
        comparison_data['phone1']['disadvantages'].append('Less RAM: ' + str(phone1.Phone_model.memory.RAM) + 'GB vs ' + str(phone2.Phone_model.memory.RAM) + 'GB. Less RAM might impact multitasking and performance.')
    
    # ROM Comparison
    if phone1.Phone_model.memory.ROM > phone2.Phone_model.memory.ROM:
        phone1_score += 1
        comparison_data['phone1']['advantages'].append('More ROM: ' + str(phone1.Phone_model.memory.ROM) + 'GB vs ' + str(phone2.Phone_model.memory.ROM) + 'GB. More ROM allows for more storage of apps, photos, videos, etc.')
        comparison_data['phone2']['disadvantages'].append('Less ROM: ' + str(phone2.Phone_model.memory.ROM) + 'GB vs ' + str(phone1.Phone_model.memory.ROM) + 'GB. Less ROM might limit the storage of apps, photos, videos, etc.')
    elif phone1.Phone_model.memory.ROM < phone2.Phone_model.memory.ROM:
        phone2_score += 1
        comparison_data['phone2']['advantages'].append('More ROM: ' + str(phone2.Phone_model.memory.ROM) + 'GB vs ' + str(phone1.Phone_model.memory.ROM) + 'GB. More ROM allows for more storage of apps, photos, videos, etc.')
        comparison_data['phone1']['disadvantages'].append('Less ROM: ' + str(phone1.Phone_model.memory.ROM) + 'GB vs ' + str(phone2.Phone_model.memory.ROM) + 'GB. Less ROM might limit the storage of apps, photos, videos, etc.')

    # Battery Size Comparison
    if phone1.Phone_model.battery.size > phone2.Phone_model.battery.size:
        phone1_score += 1
        comparison_data['phone1']['advantages'].append('Larger Battery: ' + str(phone1.Phone_model.battery.size) + 'mAh vs ' + str(phone2.Phone_model.battery.size) + 'mAh. A larger battery can provide longer usage time.')
        comparison_data['phone2']['disadvantages'].append('Smaller Battery: ' + str(phone2.Phone_model.battery.size) + 'mAh vs ' + str(phone1.Phone_model.battery.size) + 'mAh. A smaller battery might need more frequent charging.')
    elif phone1.Phone_model.battery.size < phone2.Phone_model.battery.size:
        phone2_score += 1
        comparison_data['phone2']['advantages'].append('Larger Battery: ' + str(phone2.Phone_model.battery.size) + 'mAh vs ' + str(phone1.Phone_model.battery.size) + 'mAh. A larger battery can provide longer usage time.')
        comparison_data['phone1']['disadvantages'].append('Smaller Battery: ' + str(phone1.Phone_model.battery.size) + 'mAh vs ' + str(phone2.Phone_model.battery.size) + 'mAh. A smaller battery might need more frequent charging.')

    # Display Size Comparison
    if phone1.Phone_model.display.size_inches > phone2.Phone_model.display.size_inches:
        phone1_score += 1
        comparison_data['phone1']['advantages'].append('Larger Display: ' + str(phone1.Phone_model.display.size_inches) + '" vs ' + str(phone2.Phone_model.display.size_inches) + '". A larger display provides a better viewing experience.')
        comparison_data['phone2']['disadvantages'].append('Smaller Display: ' + str(phone2.Phone_model.display.size_inches) + '" vs ' + str(phone1.Phone_model.display.size_inches) + '". A smaller display may not be as immersive.')
    elif phone1.Phone_model.display.size_inches < phone2.Phone_model.display.size_inches:
        phone2_score += 1
        comparison_data['phone2']['advantages'].append('Larger Display: ' + str(phone2.Phone_model.display.size_inches) + '" vs ' + str(phone1.Phone_model.display.size_inches) + '". A larger display provides a better viewing experience.')
        comparison_data['phone1']['disadvantages'].append('Smaller Display: ' + str(phone1.Phone_model.display.size_inches) + '" vs ' + str(phone2.Phone_model.display.size_inches) + '". A smaller display may not be as immersive.')

    # Camera Comparison
    if phone1.Phone_model.main_camera.module > phone2.Phone_model.main_camera.module:
        phone1_score += 1
        comparison_data['phone1']['advantages'].append('Higher Resolution Main Camera: ' + str(phone1.Phone_model.main_camera.module) + 'MP vs ' + str(phone2.Phone_model.main_camera.module) + 'MP. A higher resolution camera can capture more detailed photos.')
        comparison_data['phone2']['disadvantages'].append('Lower Resolution Main Camera: ' + str(phone2.Phone_model.main_camera.module) + 'MP vs ' + str(phone1.Phone_model.main_camera.module) + 'MP. A lower resolution camera may not capture photos as detailed.')
    elif phone1.Phone_model.main_camera.module < phone2.Phone_model.main_camera.module:
        phone2_score += 1
        comparison_data['phone2']['advantages'].append('Higher Resolution Main Camera: ' + str(phone2.Phone_model.main_camera.module) + 'MP vs ' + str(phone1.Phone_model.main_camera.module) + 'MP. A higher resolution camera can capture more detailed photos.')
        comparison_data['phone1']['disadvantages'].append('Lower Resolution Main Camera: ' + str(phone1.Phone_model.main_camera.module) + 'MP vs ' + str(phone2.Phone_model.main_camera.module) + 'MP. A lower resolution camera may not capture photos as detailed.')

    # Selfie Camera Comparison
    if phone1.Phone_model.selfi_camera.module > phone2.Phone_model.selfi_camera.module:
        phone1_score += 1
        comparison_data['phone1']['advantages'].append('Higher Resolution Selfie Camera: ' + str(phone1.Phone_model.selfi_camera.module) + 'MP vs ' + str(phone2.Phone_model.selfi_camera.module) + 'MP. A higher resolution selfie camera can capture more detailed photos.')
        comparison_data['phone2']['disadvantages'].append('Lower Resolution Selfie Camera: ' + str(phone2.Phone_model.selfi_camera.module) + 'MP vs ' + str(phone1.Phone_model.selfi_camera.module) + 'MP. A lower resolution selfie camera may not capture photos as detailed.')
    elif phone1.Phone_model.selfi_camera.module < phone2.Phone_model.selfi_camera.module:
        phone2_score += 1
        comparison_data['phone2']['advantages'].append('Higher Resolution Selfie Camera: ' + str(phone2.Phone_model.selfi_camera.module) + 'MP vs ' + str(phone1.Phone_model.selfi_camera.module) + 'MP. A higher resolution selfie camera can capture more detailed photos.')
        comparison_data['phone1']['disadvantages'].append('Lower Resolution Selfie Camera: ' + str(phone1.Phone_model.selfi_camera.module) + 'MP vs ' + str(phone2.Phone_model.selfi_camera.module) + 'MP. A lower resolution selfie camera may not capture photos as detailed.')

    # Waterproof Comparison
    if phone1.Phone_model.is_waterproof and not phone2.Phone_model.is_waterproof:
        phone1_score += 1
        comparison_data['phone1']['advantages'].append('Waterproof: Phone1 is waterproof while Phone2 is not. A waterproof phone is beneficial for accidental spills or usage in rainy weather.')
        comparison_data['phone2']['disadvantages'].append('Not Waterproof: Phone2 is not waterproof while Phone1 is. A non-waterproof phone requires extra care around liquids.')
    elif not phone1.Phone_model.is_waterproof and phone2.Phone_model.is_waterproof:
        phone2_score += 1
        comparison_data['phone2']['advantages'].append('Waterproof: Phone2 is waterproof while Phone1 is not. A waterproof phone is beneficial for accidental spills or usage in rainy weather.')
        comparison_data['phone1']['disadvantages'].append('Not Waterproof: Phone1 is not waterproof while Phone2 is. A non-waterproof phone requires extra care around liquids.')
   
    # Fast Charging Comparison
    if phone1.Phone_model.battery.fast_charging and not phone2.Phone_model.battery.fast_charging:
        phone1_score += 1
        comparison_data['phone1']['advantages'].append('Fast Charging')
        comparison_data['phone2']['disadvantages'].append('No Fast Charging')
    elif not phone1.Phone_model.battery.fast_charging and phone2.Phone_model.battery.fast_charging:
        phone2_score += 1
        comparison_data['phone2']['advantages'].append('Fast Charging')
        comparison_data['phone1']['disadvantages'].append('No Fast Charging')

    if phone1_score > phone2_score:
        winner = phone1
        difference = phone1_score - phone2_score
    elif phone2_score > phone1_score:
        winner = phone2
        difference = phone2_score - phone1_score
    else:
        winner = "Tie"
        difference = 0

    user = request.user if request.user.is_authenticated else None
    # Create a new instance of ComparisonHistory
    if user:
        phone1_name = phone1.name
        phone2_name = phone2.name
        comparison_result = winner
        comparison_date = timezone.now()

        # Save the comparison result to the database
        comparison = ComparisonHistory(
        user=user,
        phone_1=phone1_name,
        phone_2=phone2_name,
        comparison_result=comparison_result,
        comparison_date=comparison_date
        )
        comparison.save()
    # Render HTML template with comparison values, winner, and difference
    context = {
        'phone1': phone1,
        'phone2': phone2,
        'score1': phone1_score,
        'score2': phone2_score,
        'winner': winner,
        'difference': difference,
        'comparison_data': comparison_data
    }
    return render(request, 'user/phone_compare.html', context)

def blog_veiw(request):
    try:
        latest_blog = Blog.objects.first()
        blogs = Blog.objects.all().exclude(id = latest_blog.id)
    except:
        latest_blog  = None
        blogs = None
    print(blogs)
    print('hello')
    paginator = Paginator(blogs, 9)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'latest_blog' : latest_blog,
        'blogs' : page,
        
    }
    return render(request, 'user/blog.html', context)


def single_blog_view(request, slug):
    blog = Blog.objects.filter(slug = slug).first()
    latest_post = Blog.objects.all().exclude(slug = slug)[:4]
    comments =  Comment.objects.filter(blog__pk = blog.pk)
    # print(latest_post)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.save()
            messages.success(request, 'Your comment has been successfully sent!')
            form = CommentForm()

    context = {
        'blog' : blog,
        'latest_posts' : latest_post,
        'form' : form,
        'comments' : comments
    }
    return render(request, 'user/blog-post.html', context)

# def contact(request):
#     contact = Contact.objects.all().first()
#     if request.method == 'POST':
#         form = ContactForm(request.POST)  
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your request has been successfully sent')
#             form = ContactForm()
#     else:
#         form = ContactForm()


#     context = {
#         'social_medias' : social_medias,
#         'contact' : contact,
#         'form' : form
#     }
    return render(request, 'Company/contact.html', context)

def about(request):
    return render(request,"user/about.html")

def contact(request):
    return render(request,"user/contacts.html")

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
    form = ReviewForm
    context = {
        'form':form,
        'phone': phone,
        'reviews': reviews,
    }
    return render(request, 'user/review.html', context)

def smart(request):
    displaylist=Phone.objects.all()
    return render(request,"user/smartphones.html",{'smarthpone':displaylist})

def smartdetail(request, pk):
    phone_list = Phone.objects.all()
    phone = Phone.objects.get(id=pk)
    return render(request, "user/smart-detail.html", {'phone': phone,'list':phone_list})

def user_profile(request):
    comparison_history = ComparisonHistory.objects.filter(user=request.user)
    context = {'comparison_history': comparison_history,'user_profile': request.user}
    return render(request, 'user/user_profile.html', context)

# ================================================= admin pages =========================================
@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class AdminIndexView(View):
    def get(self, request):
        brand_names = brand.objects.filter().values_list('brand',flat=True)
        count_names = brand.objects.filter()
        brands = list(brand_names)
        print(brands)
        no_of_brand = []
        for i in count_names:
            numbers = i.count_phone()
            no_of_brand.append(numbers)
        print(no_of_brand)

        count_user = CustomUser.objects.filter(is_user = True).count()
        count_admin = CustomUser.objects.filter(is_superuser = True).count()

        context ={'names':brands,'counts':no_of_brand,'users':count_user,'admins':count_admin}
        return render(request, 'myadmin/index.html',context)
# # ================================================  delet =======================================
@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class UserDeleteView(DeleteView):
    model = CustomUser
    success_url = reverse_lazy('user_list')
    http_method_names = ['post']

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ModelDeleteView(View):
    def post(self, request, pk):
        model = get_object_or_404(model, pk=pk)
        model.delete()
        return redirect('model_list')

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class AnnounceDeleteView(DeleteView):
    model = anounnced
    success_url = reverse_lazy('list_announce_url')
    http_method_names = ['post']

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class PlatformDeleteView(DeleteView):
    model = Plattform
    success_url = reverse_lazy('list_announce_url')
    http_method_names = ['post']

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ResolutionDeleteView(DeleteView):
    model = Resolution
    success_url = reverse_lazy('list_announce_url')
    http_method_names = ['post']
      
@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')      
class BatteryDeleteView(DeleteView):
    model = Battery
    success_url = reverse_lazy('list_battery_url')
    http_method_names = ['post']

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')    
class BodyDeleteView(DeleteView):
    model = Body
    success_url = reverse_lazy('list_body_url')
    http_method_names = ['post']

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class BrandDeleteView(DeleteView):
    model = brand
    success_url = reverse_lazy('list_brand_url')
    http_method_names = ['post']

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class CameraDeleteView(DeleteView):
    model = Camera
    success_url = reverse_lazy('list_camera_url')
    http_method_names = ['post']

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ConnectivityDeleteView(DeleteView):
    model = Connectivity
    success_url = reverse_lazy('list_connectivity_url')
    http_method_names = ['post']
    
@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')   
class DimensionDeleteView(DeleteView):
    model = Dimensions
    success_url = reverse_lazy('list_dimension_url')
    http_method_names = ['post']

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')   
class DisplayDeleteView(DeleteView):
    model = Display
    success_url = reverse_lazy('list_display_url')
    http_method_names = ['post']

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')    
class MemoryDeleteView(DeleteView):
    model = Memory
    success_url = reverse_lazy('list_memory_url')
    http_method_names = ['post']

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class RsolutionDeleteView(DeleteView):
    model = Resolution
    success_url = reverse_lazy('list_resolution_url')
    http_method_names = ['post']

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'myadmin/user_managment/list_user.html'
    context_object_name = 'users'
# ============================================== update =============================================
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

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'myadmin/user_managment/create_user.html'
    form_class = AdminCreationForm
    success_url = reverse_lazy('user_list')

# ============================================== Add model =============================================
# @method_decorator(login_required, name='dispatch')
class UserCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    template_name = 'myadmin/user_managment/create_user.html'
    form_class = AdminCreationForm
    success_url = reverse_lazy('user_list')

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
def phoneList(request):
    displaylist=Phone.objects.all()
    return render(request,"myadmin/phone_list.html",{'data':displaylist})

class ModelListView(View):
    def get(self, request):
        models = model.objects.all()
        return render(request, 'myadmin/model_list.html', {'models': models})

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


