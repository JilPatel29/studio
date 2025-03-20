from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
     path('booking/', views.booking, name='booking'),
    path('process-booking/', views.process_booking, name='process_booking'),
    path('payment-callback/', views.payment_callback, name='payment_callback'),
    path('booking-confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('add-testimonial/', views.add_testimonial, name='add_testimonial'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns = [
#     path('', views.index, name='index'),
#     path('home/', views.home, name='home'),
#     path('gallery/', views.gallery, name='gallery'),
#     path('contact/', views.contact, name='contact'),
#     path('services/', views.services, name='services'),
#     path('booking/', views.booking, name='booking'),
#     path('process-booking/', views.process_booking, name='process_booking'),
#     path('blog/', views.blog, name='blog'),
#     path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),  # Updated this line
#     path('signup/', views.signup_view, name='signup'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('profile/', views.profile_view, name='profile'),
#     # path('verify-otp/', views.verify_otp, name='verify_otp'),
#     path('add-testimonial/', views.add_testimonial, name='add_testimonial'),
#     path('edit-profile/', views.edit_profile, name='edit_profile'),
#     path('verify-email-otp/', views.verify_email_otp, name='verify_email_otp'),
#     # path('verify-phone-otp/', views.verify_phone_otp, name='verify_phone_otp'),


# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)