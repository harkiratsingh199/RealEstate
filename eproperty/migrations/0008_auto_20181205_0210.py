# Generated by Django 2.1.4 on 2018-12-05 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eproperty', '0007_auto_20181205_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyimage',
            name='propertyImage',
            field=models.ImageField(blank=True, null=True, upload_to='uploadedImage/'),
        ),
    ]