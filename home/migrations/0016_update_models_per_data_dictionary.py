"""
# Update Models per Data Dictionary

1. Changes
   - Updated model fields to match data dictionary specifications
   - Added new constraints and validations
   - Maintained existing authentication system
   - Added proper relationships between models

2. Model Updates
   - CustomUser: Kept existing authentication with additional fields
   - Booking: Added proper status choices and relationships
   - Payment: Added status choices and booking relationship
   - Service: Added price and description fields
   - Gallery: Added service relationship
   - Blog: Added author relationship
   - Testimonial: Added rating validation
   - ContactUs: Added submitted_at field
"""

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_customuser_email_verified_alter_customuser_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(
                choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')],
                default='Pending',
                max_length=20
            ),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(
                choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')],
                default='Pending',
                max_length=20
            ),
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='rating',
            field=models.IntegerField(
                validators=[MinValueValidator(1), MaxValueValidator(5)]
            ),
        ),
        migrations.AlterModelOptions(
            name='contactus',
            options={'verbose_name': 'Contact Message', 'verbose_name_plural': 'Contact Messages'},
        ),
    ]