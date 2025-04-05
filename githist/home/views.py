from functools import cache
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from core import settings
from .models import ContactUs, Service, Blog, Gallery, Testimonial
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
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
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Booking, Payment, Package
import razorpay
import json
import hmac
import hashlib


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
    testimonials = Testimonial.objects.filter(is_displayed=True).order_by('-date_submitted')[:3]
    
    # Get gallery items
    gallery_items = Gallery.objects.all().order_by('-uploaded_at')[:6]
    
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
    testimonials = Testimonial.objects.filter(is_displayed=True).order_by('-date_submitted')[:3]
    gallery_items = Gallery.objects.all().order_by('-uploaded_at')[:6]
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
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        
        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']
        
        user.save()
        return redirect('home')
        
    return render(request, 'edit_profile.html')

@login_required
def add_testimonial(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        rating = request.POST.get('rating')
        
        if message and rating:
            testimonial = Testimonial.objects.create(
                customer_name=request.user.username,
                message=message,
                rating=int(rating),
                customer=request.user.username,
                is_displayed=False  # Requires admin approval
            )
            messages.success(request, 'Thank you for your review! It will be displayed after approval.')
        else:
            messages.error(request, 'Please provide both a message and rating.')
        
        return redirect('home')
    return redirect('home')

def services(request):
    active_services = Service.objects.filter(is_active=True).order_by('name')
    return render(request, "services.html", {'services': active_services})

def gallery(request):
    categories = {
        'wedding': Gallery.objects.filter(category='wedding'),
        'prewedding': Gallery.objects.filter(category='prewedding'),
        'birthday': Gallery.objects.filter(category='birthday'),
        'outdoor': Gallery.objects.filter(category='outdoor'),
        'maternity': Gallery.objects.filter(category='maternity'),
    }
    return render(request, 'gallery.html', {'categories': categories})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        contact = ContactUs(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        contact.save()
        
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
        
    return render(request, "contact.html")

def blog(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, "blog.html", {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, "blog_detail.html", {'blog': blog})
razorpay_client = razorpay.Client(
    auth=("rzp_test_38CgcUEr3zKkc7", "RyozxVs6ONs9qdaGcuLWyaUo")
)

@login_required
def booking(request):
    packages = Package.objects.all()
    context = {
        'packages': packages
    }
    return render(request, 'booking.html', context)

@login_required
def process_booking(request):
    if request.method == "POST":
        try:
            # Get form data
            package_id = request.POST.get('package')
            booking_date = request.POST.get('booking_date')
            booking_time = request.POST.get('booking_time')
            payment_method = request.POST.get('payment_method')
            phone = request.POST.get('phone')
            
            # Get the package
            package = Package.objects.get(id=package_id)
            
            custom_user = CustomUser.objects.get(id=request.user.id)
            
            # Create booking
            booking = Booking.objects.create(
                customer=custom_user,
                customer_name=custom_user.username,
                customer_email=custom_user.email,
                customer_phone=phone,
                package=package,
                booking_date=booking_date,
                booking_time=booking_time,
                total_amount=package.price,
                status='pending'
            )
    

            # Handle different payment methods
            if payment_method == 'cash':
                # Create payment record for cash
                Payment.objects.create(
                    booking=booking,
                    amount=package.price,
                    payment_method='cash',
                    payment_status='pending'
                )
                return JsonResponse({
                    'status': 'success',
                    'message': 'Booking confirmed for cash payment',
                    'redirect_url': '/booking-confirmation/'
                })
            else:
                # Create Razorpay order for online payments
                amount_in_paise = int(float(package.price) * 100)  # Convert to paise
                order_currency = 'INR'
                order_receipt = f'order_rcptid_{booking.id}'
                
                razorpay_order = razorpay_client.order.create({
                    'amount': amount_in_paise,
                    'currency': order_currency,
                    'receipt': order_receipt,
                })

                # Create payment record
                Payment.objects.create(
                    booking=booking,
                    amount=package.price,
                    payment_method=payment_method,
                    payment_status='pending',
                    razorpay_order_id=razorpay_order['id']
                )

                return JsonResponse({
                    'status': 'success',
                    'order_id': razorpay_order['id'],
                    'amount': amount_in_paise,
                    'currency': order_currency
                })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })

@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            payment_id = data.get('razorpay_payment_id')
            order_id = data.get('razorpay_order_id')
            signature = data.get('razorpay_signature')
            
            params_dict = {
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': order_id,
                'razorpay_signature': signature
            }
            
            try:
                # Verify payment signature
                razorpay_client.utility.verify_payment_signature(params_dict)
                
                # Update payment status
                payment = Payment.objects.get(razorpay_order_id=order_id)
                payment.payment_status = 'completed'
                payment.razorpay_payment_id = payment_id
                payment.razorpay_signature = signature
                payment.save()
                
                # Update booking status
                booking = payment.booking
                booking.status = 'confirmed'
                booking.save()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Payment successful'
                })
            except razorpay.errors.SignatureVerificationError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid payment signature'
                })
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
            
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })

def booking_confirmation(request):
    return render(request, 'booking_confirmation.html')

# Keep all other view functions unchanged