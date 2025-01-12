import os
import re
from account.models import *
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, URLValidator, EmailValidator

class Category(models.Model):
    """
    Model representing a category for organizing content or users.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate a unique slug if not provided
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super(Category, self).save(*args, **kwargs)

    def generate_unique_slug(self):
        """
        Generates a unique slug from the category's name.
        If the slug already exists, appends a numerical suffix to make it unique.
        """
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

def user_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return f'profile_images/user_{slugify(instance.slug)}_{instance.phone_number}{file_extension}'

class Place(models.Model):
    """
    Model representing a place where users can grab food or drinks.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='place', null=True, blank=True, verbose_name=_('Associated User'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='places', verbose_name=_('Category'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    province = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('Province'))
    district = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('District'))
    sector = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('Sector'))
    cell = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('Cell'))
    village = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('Village'))
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('Address'))
    latitude = models.FloatField(validators=[RegexValidator(regex=r'^-?([1-8]?\d(\.\d+)?|90(\.0+)?)$', message='Enter a valid latitude (-90 to 90).')], null=True, blank=True, verbose_name=_('Latitude'))
    longitude = models.FloatField(validators=[RegexValidator(regex=r'^-?((1[0-7]\d)|(\d{1,2}))(\.\d+)?$', message='Enter a valid longitude (-180 to 180).')], null=True, blank=True, verbose_name=_('Longitude'))
    main_phone_number = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Enter a valid phone number (up to 15 digits).')], null=True, blank=True, verbose_name=_('Main Phone Number'))
    second_phone_number = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Enter a valid phone number (up to 15 digits).')], blank=True, null=True, verbose_name=_('Second Phone Number'))
    email = models.EmailField(validators=[EmailValidator()], unique=True, null=True, blank=True, verbose_name=_('Email'))
    instagram = models.URLField(validators=[URLValidator()], blank=True, null=True, verbose_name=_('Instagram URL'))
    whatsapp = models.URLField(validators=[URLValidator()], blank=True, null=True, verbose_name=_('WhatsApp URL'))
    tiktok = models.URLField(validators=[URLValidator()], blank=True, null=True, verbose_name=_('TikTok URL'))
    facebook = models.URLField(validators=[URLValidator()], blank=True, null=True, verbose_name=_('Facebook URL'))
    twitter = models.URLField(validators=[URLValidator()], blank=True, null=True, verbose_name=_('Twitter URL'))
    profile_image = ProcessedImageField(
        upload_to=user_image_path,
        processors=[ResizeToFill(720, 720)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True,
        verbose_name=_('Profile Image')
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')
        ordering = ['created_at']

    def __str__(self):
        return self.user.name if self.user else self.address

    def clean(self):
        """
        Custom validation for the Place model.
        """
        super().clean()
        if not self.user and not self.email:
            raise ValidationError(_('Email is required if no user is associated.'))
        # Additional custom validations can be added here.

    def save(self, *args, **kwargs):
        """
        Overrides the save method to handle User creation/updation.
        """
        # Determine if this is a new instance
        is_new = self.pk is None

        super(Place, self).save(*args, **kwargs)

        if not self.user:
            # Create a new User with role 'Client'
            user = User.objects.create(
        email=self.email,         name=self.user_name if hasattr(self, 'user_name') else self.address,  # Default to address if name not provided
                phone_number=self.main_phone_number,         role='Client',         slug=slugify(self.user_name) if hasattr(self, 'user_name') else slugify(self.address)
            )
            if self.profile_image:
                user.image = self.profile_image
                user.save()
            self.user = user
            super(Place, self).save(update_fields=['user'])

    @property
    def user_name(self):
        """
        Returns the name of the user associated with the place.
        Defaults to the address if not provided.
        """
        return getattr(self, '_user_name', self.address)

    @user_name.setter
    def user_name(self, value):
        self._user_name = value