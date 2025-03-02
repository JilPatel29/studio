from functools import cache
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from core import settings
from .models import Contact, Service, Blog, Gallery, Testimonial, Booking, Payment
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, ContactForm, BookingForm, TestimonialForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
import random
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.db.models import Q

def generate_otp():
    return str(random.randint(100000, 999999))

def send_verification_email(email, otp):
    subject = 'Email Verification OTP'
    message = f'Your OTP for email verification is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validation
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(request, 'signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, 'signup.html')

        # Create inactive user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.is_active = False
        user.save()

        # Generate and store OTP
        otp = generate_otp()
        request.session['email_otp'] = otp
        request.session['user_id'] = user.id

        # Send verification email
        send_verification_email(email, otp)
        
        messages.success(request, "Please check your email for verification code")
        return redirect('verify_email')

    return render(request, 'signup.html')

def verify_email(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        stored_otp = request.session.get('email_otp')
        user_id = request.session.get('user_id')

        if user_otp == stored_otp:
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()

            # Clear session
            del request.session['email_otp']
            del request.session['user_id']

            messages.success(request, "Email verified successfully! Please login.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'verify_email.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Successfully logged in!")
                return redirect('home')
            else:
                messages.error(request, "Please verify your email first")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('home')

def index(request):
    # Get latest approved testimonials
    testimonials = Testimonial.objects.all().order_by('-testimonial_id')[:3]
    
    # Get gallery items
    gallery_items = Gallery.objects.all().order_by('-image_id')[:6]
    
    # Get services
    services = Service.objects.all()
    
    context = {
        'testimonials': testimonials,
        'gallery_items': gallery_items,
        'services': services,
    }
    
    return render(request, 'index.html', context)

def home(request):
    # Similar to index view
    testimonials = Testimonial.objects.all().order_by('-testimonial_id')[:3]
    gallery_items = Gallery.objects.all().order_by('-image_id')[:6]
    services = Service.objects.all()
    
    context = {
        'testimonials': testimonials,
        'gallery_items': gallery_items,
        'services': services,
    }
    
    return render(request, 'home.html', context)

def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def admin_view(request):
    return redirect('/admin/')

@login_required
def profile_view(request):
    # Get user's bookings
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    
    # Get user's testimonials
    testimonials = Testimonial.objects.filter(user=request.user)
    
    context = {
        'bookings': bookings,
        'testimonials': testimonials
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        
        # Update username if provided
        new_username = request.POST.get('username')
        if new_username and new_username != user.username:
            if CustomUser.objects.filter(username=new_username).exclude(id=user.id).exists():
                messages.error(request, 'Username already taken.')
                return redirect('edit_profile')
            user.username = new_username
            
        # Update phone number if provided
        new_phone = request.POST.get('phone_number')
        if new_phone:
            user.phone_number = new_phone
            
        # Update profile picture if provided
        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']
            
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('home')
        
    return render(request, 'edit_profile.html')

@login_required
def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TestimonialForm()
    
    return render(request, 'add_testimonial.html', {'form': form})

def services(request):
    services_list = Service.objects.all().order_by('name')
    return render(request, "services.html", {'services': services_list})

def gallery(request):
    gallery_items = Gallery.objects.all()
    return render(request, 'gallery.html', {'gallery_items': gallery_items})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
        
    return render(request, "contact.html", {'form': form})

@login_required
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Booking created successfully!')
            return redirect('booking_success')
    else:
        form = BookingForm()
    
    return render(request, 'booking.html', {'form': form})

def blog(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, "blog.html", {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, blog_id=blog_id)
    return render(request, "blog_detail.html", {'blog': blog})

def process_booking(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        service = request.POST.get('service')
        date_time = request.POST.get('date_time')
        payment_method = request.POST.get('payment_method')

        return HttpResponse(f"Thank you {first_name} {last_name}, your booking for {service} on {date_time} has been received! Payment method: {payment_method}.")
    else:
        return redirect('booking')

def booking_success(request):
    return render(request, 'booking_success.html')