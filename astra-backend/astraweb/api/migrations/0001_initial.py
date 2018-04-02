# Generated by Django 2.0.3 on 2018-04-02 01:39

import api.models.project
import api.models.user
from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('logged_in', models.BooleanField(default=False, verbose_name='logged_in')),
                ('username', models.CharField(default='0', max_length=1)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=150, null=True)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser')),
                ('street_addr1', models.CharField(blank=True, max_length=100, null=True)),
                ('street_addr2', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=40, null=True)),
                ('state', models.CharField(blank=True, max_length=2, null=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='State ID length must be 2 characters', regex='^\\w{2}$')])),
                ('country', models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='Country code length must be 2 characters', regex='^\\w{2}$')])),
                ('zip_code', models.PositiveIntegerField(blank=True, null=True)),
                ('id_file', models.ImageField(blank=True, null=True, upload_to='')),
                ('selfie', models.ImageField(blank=True, null=True, upload_to='./selfies')),
                ('ether_addr', models.CharField(blank=True, max_length=40, null=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='Ether address length must be 40 characters', regex='^\\w{40}$')])),
                ('ether_part_amount', models.PositiveIntegerField(blank=True, null=True)),
                ('telegram_addr', models.CharField(blank=True, max_length=50, null=True)),
                ('bitcoin_balance', models.DecimalField(decimal_places=4, default=0, max_digits=11, validators=[django.core.validators.MinValueValidator(Decimal('0.0000'))])),
                ('ether_balance', models.DecimalField(decimal_places=4, default=0, max_digits=11, validators=[django.core.validators.MinValueValidator(Decimal('0.0000'))])),
                ('usd_balance', models.DecimalField(decimal_places=2, default=0, max_digits=11, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('star_balance', models.DecimalField(decimal_places=2, default=0, max_digits=11, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('start_time', models.DateField(auto_now_add=True)),
                ('user_type', models.PositiveSmallIntegerField(choices=[(0, 'None'), (1, 'Investor'), (2, 'Contributor'), (3, 'Both')], default=0)),
                ('email_verified', models.BooleanField(default=False)),
                ('phone_verified', models.BooleanField(default=False)),
                ('twitter_name', models.CharField(blank=True, max_length=50, null=True)),
                ('facebook_url', models.URLField(blank=True, null=True)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
                ('bitcoin_name', models.CharField(blank=True, max_length=50, null=True)),
                ('reddit_name', models.CharField(blank=True, max_length=50, null=True)),
                ('steemit_name', models.CharField(blank=True, max_length=50, null=True)),
                ('referral_code', models.CharField(blank=True, max_length=150, null=True)),
                ('referral_type', models.PositiveSmallIntegerField(choices=[(0, 'No Referral'), (1, 'Google'), (2, 'Email Marketing'), (3, 'Facebook'), (4, 'Referral')], default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'db_table': 'api_user',
            },
            managers=[
                ('objects', api.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, default='', max_length=40, validators=[django.core.validators.RegexValidator(code='nomatch', message='UID length (from SHA1) must be 40 characters', regex='^\\w{40}$')])),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
                ('company', models.CharField(max_length=45)),
                ('model', models.CharField(max_length=30)),
                ('run_on_batteries', models.BooleanField(default=False)),
                ('run_if_active', models.BooleanField(default=False)),
                ('start_hour', models.SmallIntegerField(blank=True, default=0, validators=[django.core.validators.MaxValueValidator(23), django.core.validators.MinValueValidator(0)])),
                ('end_hour', models.SmallIntegerField(blank=True, default=23, validators=[django.core.validators.MaxValueValidator(23), django.core.validators.MinValueValidator(0)])),
                ('max_CPUs', models.SmallIntegerField(blank=True, default=2, validators=[django.core.validators.MaxValueValidator(8), django.core.validators.MinValueValidator(0)])),
                ('disk_max_percent', models.SmallIntegerField(blank=True, default=50, validators=[django.core.validators.MaxValueValidator(0), django.core.validators.MinValueValidator(100)])),
                ('ram_max_percent', models.SmallIntegerField(blank=True, default=50, validators=[django.core.validators.MaxValueValidator(0), django.core.validators.MinValueValidator(100)])),
                ('cpu_max_percent', models.SmallIntegerField(blank=True, default=50, validators=[django.core.validators.MaxValueValidator(0), django.core.validators.MinValueValidator(100)])),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'api_device',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=300, null=True, unique=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('sponsors', api.models.project.SeparatedValuesField(null=True)),
                ('description', models.TextField(null=True)),
                ('area1', models.CharField(max_length=50, null=True)),
                ('area2', models.CharField(blank=True, max_length=50, null=True)),
                ('platforms', api.models.project.PlatformField(max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('duration', models.DurationField()),
                ('actionable', models.BooleanField(default=False)),
                ('markdown', models.SmallIntegerField(blank=True, default=0, validators=[django.core.validators.MaxValueValidator(0), django.core.validators.MinValueValidator(100)])),
            ],
            options={
                'db_table': 'api_sale',
            },
        ),
        migrations.CreateModel(
            name='SocialMediaPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='UID must be 10 hex characters', regex='^\\w{10}$')])),
                ('platform', models.CharField(choices=[('FB', 'Facebook'), ('TW', 'Twitter'), ('TE', 'Telegram'), ('LN', 'Linkedin'), ('BT', 'Bitcoin Talk'), ('RD', 'Reddit'), ('OR', 'Other')], default='OR', max_length=2)),
                ('content', models.TextField()),
                ('date', models.DateTimeField()),
                ('verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete='CASCADE', related_name='post', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'api_social_media_post',
            },
        ),
        migrations.AddField(
            model_name='device',
            name='active_projects',
            field=models.ManyToManyField(blank=True, related_name='active_projects', to='api.Project'),
        ),
        migrations.AddField(
            model_name='device',
            name='dormant_projects',
            field=models.ManyToManyField(blank=True, related_name='dormant_projects', to='api.Project'),
        ),
        migrations.AddField(
            model_name='device',
            name='past_projects',
            field=models.ManyToManyField(blank=True, related_name='past_projects', to='api.Project'),
        ),
        migrations.AddField(
            model_name='device',
            name='user',
            field=models.ForeignKey(blank=True, on_delete='CASCADE', related_name='device', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='projects',
            field=models.ManyToManyField(blank=True, to='api.Project'),
        ),
        migrations.AddField(
            model_name='user',
            name='referral_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referral', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
