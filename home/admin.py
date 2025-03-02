from django.contrib import admin
from .models import (
    Service,
    Booking,
    Payment,
    Blog,
    Gallery,
    Testimonial,
    Contact,
    CustomUser
)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'name', 'price')
    search_fields = ('name', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'service', 'booking_date', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('user__username', 'service__name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'booking', 'amount', 'payment_date', 'status')
    list_filter = ('status', 'payment_date')
    search_fields = ('booking__booking_id',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog_id', 'title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'content')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'service', 'image_url')
    list_filter = ('service',)
    search_fields = ('service__name',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('testimonial_id', 'user', 'rating')
    list_filter = ('rating',)
    search_fields = ('user__username', 'feedback')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'name', 'email', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'message')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_active', 'email_verified')
    list_filter = ('is_active', 'email_verified')
    search_fields = ('username', 'email', 'phone_number')