from django.conf import settings
from django.urls import path
from. import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/',views.Registeruserview,name='user_registration'),
    path('admin/register/',views.Registeradminview,name='Admin_registration'),
    # path('login/',views.login,name='login'),
    path('login/',jwt_views.TokenObtainPairView.as_view(),name='login'),
    path('login/refresh/',jwt_views.TokenRefreshView.as_view(),name='refresh'),
    path('admin/application_list/',views.application_list,name='application_list'),
    path('home/',views.home,name='home'),
    path('admin/',views.admin,name='admin'),
    path('application/',views.slot_application,name='slot_application'),
    path('bookslot/<int:application_no>/<int:slot_no>/',views.book_slot,name='bookslot'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
