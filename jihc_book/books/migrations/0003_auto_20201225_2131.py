# Generated by Django 3.1.4 on 2020-12-25 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20201224_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='poster',
            field=models.ImageField(upload_to='books/', verbose_name='Постер'),
        ),
    ]
