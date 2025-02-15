from functools import cache
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
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

# def send_otp_sms(phone_number, otp):
#     # For now, just print the OTP (you'll need to integrate an SMS service)
#     print(f"SMS OTP for {phone_number}: {otp}")
#     return True

# def verify_phone_otp(request):
#     if request.method == 'POST':
#         phone_otp = request.POST.get('phone_otp')
#         signup_data = request.session.get('signup_data')
        
#         if not signup_data:
#             messages.error(request, 'Session expired. Please sign up again.')
#             return redirect('signup')
        
#         stored_otp = cache.get(f'phone_otp_{signup_data["phone_number"]}')
        
#         if phone_otp == stored_otp:
#             # Create user
#             user = CustomUser.objects.create_user(
#                 username=signup_data['username'],
#                 email=signup_data['email'],
#                 phone_number=signup_data['phone_number'],
#                 password=signup_data['password']
#             )
            
#             # Clean up
#             del request.session['signup_data']
#             cache.delete(f'email_otp_{signup_data["email"]}')
#             cache.delete(f'phone_otp_{signup_data["phone_number"]}')
            
#             messages.success(request, 'Registration successful! Please login.')
#             return redirect('login')
#         else:
#             messages.error(request, 'Invalid phone OTP. Please try again.')
    
#     return render(request, 'verify_phone_otp.html')
 
# def login_view(request):
#     if request.user.is_authenticated:
#         if request.user.is_staff:
#             return redirect('/admin/')
#         return redirect('home')

#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             if user.is_staff:
#                 return redirect('/admin/')
#             return redirect('home')
#         else:
#             messages.error(request, 'Invalid username or password.')

#     return render(request, 'login.html')

# @login_required
# def logout_view(request):
#     logout(request)
#     messages.success(request, 'Successfully logged out.')
#     return redirect('login')

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


# def signup_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#         phone_number = request.POST['phone_number']

#         if password1 != password2:
#             messages.error(request, "Passwords do not match.")
#             return render(request, 'signup.html')
        
#         if CustomUser.objects.filter(username=username).exists():
#             messages.error(request, "Username already taken.")
#             return render(request, 'signup.html')

#         if CustomUser.objects.filter(email=email).exists():
#             messages.error(request, "Email already registered.")
#             return render(request, 'signup.html')

#         if CustomUser.objects.filter(phone_number=phone_number).exists():
#             messages.error(request, "Phone number already registered.")
#             return render(request, 'signup.html')

#         user = CustomUser.objects.create_user(
#             username=username, 
#             email=email, 
#             password=password1, 
#             phone_number=phone_number
#         )
#         user.save()

#         login(request, user)
#         return redirect('home')
    
#     return render(request, 'signup.html')

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Invalid username or password.')

#     return render(request, 'login.html')

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
        
        # Create and save the contact submission
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

def booking(request):
    return render(request, 'booking.html')

def blog(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, "blog.html", {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, "blog_detail.html", {'blog': blog})

# def blog(request):
#     blogs = [
#         {
#             'id': 1,
#             'title': 'The Art of Wedding Photography',
#             'content': 'Wedding photography is an art that requires both technical skill and creative vision...',
#             'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcST368j8vaV1uHWS-LGeH5mpcvIZ-Gp9FgaMA&s',
#             'short_description': 'Explore the magic moments we capture in weddings...',
#             'author': 'John Smith',
#             'date': '2024-03-15'
#         },
#         {
#             'id': 2,
#             'title': 'Creative Pre-Wedding Shoot Ideas',
#             'content': 'Pre-wedding photoshoots have become an essential part of the wedding journey...',
#             'image_url': 'https://www.weddingreels.in/wp-content/uploads/2022/01/pre-wedding3.jpg',
#             'short_description': 'Get inspired by unique themes for your pre-wedding photoshoot...',
#             'author': 'Sarah Johnson',
#             'date': '2024-03-14'
#         },
#         {
#             'id': 3,
#             'title': 'Post-Processing Tips for Flawless Photos',
#             'content': 'Post-processing is a crucial step in creating stunning photographs...',
#             'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTD8_Gv6_B6n7mlcDuBEZNUf96ELq2PsALihx8TwL7IPkesmBhpH95JZWL9NrsbHZXvlhg&usqp=CAU',
#             'short_description': 'Learn professional editing tips to bring out the best in every shot...',
#             'author': 'Mike Wilson',
#             'date': '2024-03-13'
#         }
#     ]
#     return render(request, 'blog.html', {'blogs': blogs})

# def blog_detail(request, blog_id):
#     blogs = {
#         1: {
#             'title': 'The Art of Wedding Photography',
#             'content': 'Wedding photography is an art that requires both technical skill and creative vision. A wedding photographer must capture not just images, but emotions, moments, and memories that will last a lifetime. From preparation shots in the morning to the final dance at night, each moment tells part of the couples unique story.\n \n Key aspects of wedding photography include:\n\n1. Preparation and Planning\n- Meeting with the couple beforehand\n- Understanding their vision and preferences\n- Scouting the venue for perfect shot locations\n\n2. Technical Excellence\n- Using appropriate equipment\n- Managing different lighting conditions\n- Capturing both posed and candid moments\n\n3. Storytelling Through Images\n- Creating a narrative flow\n- Capturing key moments and emotions\n- Documenting both big events and small details',
#             'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcST368j8vaV1uHWS-LGeH5mpcvIZ-Gp9FgaMA&s',
#             'author': 'John Smith',
#             'date': '2024-03-15'
#         },
#         2: {
#             'title': 'Creative Pre-Wedding Shoot Ideas',
#             'content': 'Pre-wedding photoshoots have become an essential part of the wedding journey. They offer couples a chance to create beautiful memories before their big day. Here are some creative ideas for stunning pre-wedding photos:\n\n1. Location Selection\n- Natural landscapes\n- Urban settings\n- Meaningful places for the couple\n\n2. Theme Ideas\n- Vintage romance\n- Modern minimalist\n- Fantasy and fairytale\n- Travel and adventure\n\n3. Styling Tips\n- Coordinated outfits\n- Props and accessories\n- Natural poses and interactions\n\n4. Time of Day\n- Golden hour shots\n- Blue hour magic\n- Night photography',
#             'image_url': 'https://www.weddingreels.in/wp-content/uploads/2022/01/pre-wedding3.jpg',
#             'author': 'Sarah Johnson',
#             'date': '2024-03-14'
#         },
#         3: {
#             'title': 'Post-Processing Tips for Flawless Photos',
#             'content': 'Post-processing is a crucial step in creating stunning photographs. Here are professional tips for enhancing your images:\n\n1. Basic Adjustments\n- Exposure correction\n- Color balance\n- Contrast enhancement\n\n2. Advanced Techniques\n- Skin retouching\n- Color grading\n- Background enhancement\n\n3. Consistency in Style\n- Developing a signature look\n- Batch processing\n- Presets creation\n\n4. Common Mistakes to Avoid\n- Over-processing\n- Unnatural skin tones\n- Heavy-handed effects',
#             'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTD8_Gv6_B6n7mlcDuBEZNUf96ELq2PsALihx8TwL7IPkesmBhpH95JZWL9NrsbHZXvlhg&usqp=CAU',
#             'author': 'Mike Wilson',
#             'date': '2024-03-13'
#         }
#     }
    
#     blog = blogs.get(blog_id)
#     if blog is None:
#         return redirect('blog')
        
#     return render(request, 'blog_detail.html', {'blog': blog})

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