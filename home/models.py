from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser
    Maintains compatibility with existing authentication system
    """
    email_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_active = models.BooleanField(default=False)  # Default to inactive until email verified
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, 
        related_name="customuser_permissions_set", 
        blank=True
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

class Service(models.Model):
    """
    Service model as per data dictionary
    """
    service_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    """
    Booking model as per data dictionary
    """
    BOOKING_STATUS = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ]
     
    booking_id = models.AutoField(primary_key=True)
    booking_date = models.DateTimeField(null=False)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='Pending')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    
    def __str__(self):
        return f"Booking #{self.booking_id} - {self.user.username} - {self.service.name}"

class Payment(models.Model):
    """
    Payment model as per data dictionary
    """
    PAYMENT_STATUS = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')
    ]
    
    payment_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    payment_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='Pending')
    
    def __str__(self):
        return f"Payment #{self.payment_id} for Booking #{self.booking.booking_id}"

class Contact(models.Model):
    """
    Contact model as per data dictionary
    """
    message_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=False)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.name} ({self.email})"

class Blog(models.Model):
    """
    Blog model as per data dictionary
    """
    blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=False)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    """
    Testimonial model as per data dictionary
    """
    testimonial_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='testimonials')
    feedback = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    def __str__(self):
        return f"Testimonial by {self.user.username}"

class Gallery(models.Model):
    """
    Gallery model as per data dictionary
    """
    image_id = models.AutoField(primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image_url = models.CharField(max_length=255, null=False)
    
    def __str__(self):
        return f"Image #{self.image_id} for {self.service.name}"