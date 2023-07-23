from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name='home_url'),
    path("about/",views.about,name='about_url'),
    path("smart/",views.smart,name='smart_url'),
    path("contact/",views.contact,name='contact_url'),
    path("blog/",views.blog,name='blog_url'),
    path("login/",views.login_view,name='login_url'),
    path("register/",views.register_veiw,name='register_url'),
    path("smartdetail/<int:pk>",views.smartdetail,name='detail'),
    path("blog-post/",views.blog,name='blog-post_url'),
    path("ad/",views.AdminIndexView.as_view(),name='Admin_home_url'),
    path('phone/comparison/<int:pk1>/<int:pk2>/',views.phone_comparison, name='phone_comparison'),
    # =========================== url for adding ==============================
    path("admin-phone/",views.AddPhoneView.as_view(),name='Admin_phone_url'),
    path("admin-model/",views.AddModelView.as_view(),name='Admin_model_url'),
    path("admin-resolution/",views.AddResolutionView.as_view(),name='Admin_resolution_url'),
    path("admin-platform/",views.AddPlatformView.as_view(),name='Admin_platform_url'),
    path("admin-memory/",views.AddMemoryView.as_view(),name='Admin_memory_url'),
    path("admin-display/",views.AddDisplayView.as_view(),name='Admin_display_url'),
    path("admin-dimension/",views.AddDimensionView.as_view(),name='Admin_dimension_url'),
    path("admin-connectivty/",views.AddConnectView.as_view(),name='Admin_connectivty_url'),
    path("admin-camera/",views.AddCameraView.as_view(),name='Admin_camera_url'),
    path("admin-brand/",views.AddBrandView.as_view(),name='Admin_brand_url'),
    path("admin-body/",views.AddBodyView.as_view(),name='Admin_body_url'),
    path("admin-battery/",views.AddbatteryView.as_view(),name='Admin_battery_url'),
    path("admin-announce/",views.AddAnnouncedView.as_view(),name='Admin_announce_url'),
    path("admin-list/",views.phoneList,name='Admin_list_url'),
    # ================================ update url ======================================
    path("phone-update/<int:pk>",views.Phoneupdate.as_view(),name='update_phone_url'),
    path('user-list/', views.UserListView.as_view(), name='user_list'),
    path('user-create/', views.UserCreateView.as_view(), name='user_create'),
    path('user-update/<int:pk>', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    # ============================= url for list ====================================
    path('list-announce/',views.AnnouncedListView.as_view(), name='list_announce_url'),
    path('list-battery/',views.BatteryListView.as_view(), name='list_battery_url'),
    path('list-body/',views.BodyListView.as_view(), name='list_body_url'),
    path('list-brand/',views.BrandListView.as_view(), name='list_brand_url'),
    path('list-camera/',views.CameraListView.as_view(), name='list_camera_url'),
    path('list-connectivity/',views.ConnectivityListView.as_view(), name='list_connectivity_url'),
    path('list-dimension/',views.DimensionListView.as_view(), name='list_dimension_url'),
    path('list-display/',views.DisplayListView.as_view(), name='list_display_url'),
    path('list-memory/',views.MemoryListView.as_view(), name='list_memory_url'),
    path('list-platform/',views.PlatformListView.as_view(), name='list_platform_url'),
    path('list-resolution/',views.ResolutionListView.as_view(), name='list_resolution_url'),


]
