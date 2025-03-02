"""
# Reset Database per Data Dictionary

1. Changes
   - Completely reset database structure to match data dictionary
   - Maintain CustomUser for authentication
   - Create new models with proper primary keys and relationships
   - Set up proper constraints and validations

2. Model Updates
   - CustomUser: Maintained for authentication
   - Service: Added service_id, name, description, price
   - Booking: Added booking_id, booking_date, status, user_id, service_id
   - Payment: Added payment_id, booking_id, amount, payment_date, status
   - Contact: Added message_id, name, email, message, submitted_at
   - Blog: Added blog_id, title, content, created_at
   - Testimonial: Added testimonial_id, user_id, feedback, rating
   - Gallery: Added image_id, service_id, image_url
"""

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_update_models_per_data_dictionary'),
    ]

    operations = [
        # Drop existing models
        migrations.DeleteModel(name='Profile', ),
        migrations.DeleteModel(name='Package', ),
        
        # Recreate Service model
        migrations.AlterField(
            model_name='service',
            name='service_id',
            field=models.AutoField(primary_key=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.RemoveField(
            model_name='service',
            name='image',
        ),
        migrations.RemoveField(
            model_name='service',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='service',
            name='category',
        ),
        migrations.RemoveField(
            model_name='service',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='service',
            name='updated_at',
        ),
        
        # Recreate Booking model
        migrations.AlterField(
            model_name='booking',
            name='booking_id',
            field=models.AutoField(primary_key=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='customer',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='created_at',
        ),
        
        # Recreate Payment model
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.AutoField(primary_key=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending', max_length=20),
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_method',
        ),
        
        # Rename ContactUs to Contact
        migrations.RenameModel(
            old_name='ContactUs',
            new_name='Contact',
        ),
        migrations.AlterField(
            model_name='contact',
            name='message_id',
            field=models.AutoField(primary_key=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='contact',
            name='message',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='contact',
            name='submitted_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.RemoveField(
            model_name='contact',
            name='subject',
        ),
        
        # Recreate Blog model
        migrations.AlterField(
            model_name='blog',
            name='blog_id',
            field=models.AutoField(primary_key=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='blog',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.RemoveField(
            model_name='blog',
            name='author',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='image',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='category',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='read_time',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='short_description',
        ),
        
        # Recreate Testimonial model
        migrations.AlterField(
            model_name='testimonial',
            name='testimonial_id',
            field=models.AutoField(primary_key=True),
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='rating',
            field=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]),
        ),
        migrations.RenameField(
            model_name='testimonial',
            old_name='feedback',
            new_name='feedback',
        ),
        migrations.RemoveField(
            model_name='testimonial',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='testimonial',
            name='is_active',
        ),
        
        # Recreate Gallery model
        migrations.AlterField(
            model_name='gallery',
            name='image_id',
            field=models.AutoField(primary_key=True),
        ),
        migrations.AddField(
            model_name='gallery',
            name='image_url',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='gallery',
            name='image',
        ),
        migrations.RemoveField(
            model_name='gallery',
            name='title',
        ),
        migrations.RemoveField(
            model_name='gallery',
            name='description',
        ),
        migrations.RemoveField(
            model_name='gallery',
            name='category',
        ),
        migrations.RemoveField(
            model_name='gallery',
            name='uploaded_at',
        ),
    ]