from django.contrib import admin
from .models import (
    Service,
    Booking,
    Payment,
    Blog,
    Gallery,
    Testimonial,
    ContactUs,
    CustomUser,
    Profile
)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'customer', 'service', 'booking_date', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('customer__username', 'service__name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'booking', 'amount', 'payment_date', 'status')
    list_filter = ('status', 'payment_date')
    search_fields = ('booking__booking_id',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog_id', 'title', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'service', 'title', 'uploaded_at')
    list_filter = ('service', 'uploaded_at')
    search_fields = ('title', 'description')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('testimonial_id', 'user', 'rating', 'created_at', 'is_active')
    list_filter = ('rating', 'is_active', 'created_at')
    search_fields = ('user__username', 'feedback')

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'message')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_active', 'email_verified')
    list_filter = ('is_active', 'email_verified')
    search_fields = ('username', 'email', 'phone_number')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__username', 'phone', 'address')