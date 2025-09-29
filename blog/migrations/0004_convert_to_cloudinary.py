# Generated migration file - replace the content with this
from django.db import migrations
import cloudinary.models

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),  # Change this to your latest migration number
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='featured_image',
            field=cloudinary.models.CloudinaryField(blank=True, help_text='Main image for the post', null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='blogresource',
            name='file',
            field=cloudinary.models.CloudinaryField(blank=True, null=True, verbose_name='raw'),
        ),
    ]