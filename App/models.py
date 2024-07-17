from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta

# Create your models here.


def upload_services(instance, filename):
    ext = filename.split('.')[-1]
    name = '{:%Y%m%d_%H%M%S}_{}'.format(datetime.now(), instance.name)
    return 'services/{}.{}'.format(name, ext)


def upload_articles(instance, filename):
    ext = filename.split('.')[-1]
    name = '{:%Y%m%d_%H%M%S}_{}'.format(datetime.now(), instance.slug)
    return 'articles/{}.{}'.format(name, ext)


def upload_partnerships(instance, filename):
    ext = filename.split('.')[-1]
    name = '{:%Y%m%d_%H%M%S}_{}'.format(datetime.now(), instance.name)
    return 'partnerships/{}.{}'.format(name, ext)


def upload_banners(instance, filename):
    ext = filename.split('.')[-1]
    name = '{:%Y%m%d_%H%M%S}_{}'.format(datetime.now(), instance.name)
    return 'banners/{}.{}'.format(name, ext)


def upload_reviews(instance, filename):
    ext = filename.split('.')[-1]
    name = '{:%Y%m%d_%H%M%S}_{}'.format(datetime.now(), instance.name)
    return 'reviews/{}.{}'.format(name, ext)


# Services Model


class Service(models.Model):
    class ServiceObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    # Insial tabel
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(
        _('Image'), upload_to=upload_services)
    features = models.JSONField()
    status = models.CharField(
        max_length=10, choices=options, default='published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # The default manager.
    ServiceObjects = ServiceObjects()  # The custom manager.

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

# Partnerships Model


class Partnership(models.Model):

    class PartnershipObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    # Inisial Tabe;
    name = models.CharField(max_length=255)
    image = models.ImageField(
        _('Image'), upload_to=upload_partnerships)
    status = models.CharField(
        max_length=10, choices=options, default='published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # The default manager.
    PartnershipObjects = PartnershipObjects()  # The custom manager.

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


# Articles Model
class Article(models.Model):

    class ArticleObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    # inisial tabel
    title = models.CharField(max_length=255)
    image = models.ImageField(
        _('Image'), upload_to=upload_articles, null=True, blank=True)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='articles')
    status = models.CharField(
        max_length=10, choices=options, default='published')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()  # The default manager.
    ArticleObjects = ArticleObjects()  # The custom manager.

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class PricelistGroup(models.Model):

    class PricelistGroupObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    # inisial tabel
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10, choices=options, default='published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # The default manager.
    PricelistGroupObjects = PricelistGroupObjects()  # The custom manager.

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Pricelist(models.Model):

    class PricelistObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    name = models.CharField(max_length=255)
    price = models.IntegerField()
    features = models.JSONField()
    pricelistgroup = models.ForeignKey(
        PricelistGroup, on_delete=models.CASCADE, related_name='pricelist')
    status = models.CharField(
        max_length=10, choices=options, default='published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # The default manager.
    PricelistObjects = PricelistObjects()  # The custom manager.

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Banner(models.Model):
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    # inisial tabel
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(
        _('Image'), upload_to=upload_banners)
    status = models.CharField(
        max_length=10, choices=options, default='published')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(
        default=datetime.now()+timedelta(days=7))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class DetailPembuatJanji(models.Model):
    options = (
        ('online', 'Online'),
        ('offline', 'Offline'),
    )

    perusahaan = models.CharField(max_length=225, blank=False, null=False,
                                  verbose_name='Nama Perusahaan')

    alamat_perusahaan = models.CharField(max_length=225, blank=False, null=False,
                                         verbose_name='Alamat Perusahaan')

    email_perusahaan = models.CharField(max_length=225, blank=False, null=False,
                                        verbose_name='Email Perusahaan')

    nomor_perusahaan = models.CharField(max_length=225, blank=False, null=False,
                                        verbose_name='Nomor Perusahaan')

    web_perusahaan = models.CharField(max_length=225, blank=True, null=True,
                                      verbose_name='Web Perusahaan')
    meeting = models.CharField(
        max_length=225, choices=options, blank=False, null=False)

    alamat_meeting = models.CharField(max_length=225, blank=True, null=True,
                                      verbose_name='Alamat Meeting')

    rencana_tanggal = models.DateField(
        null=False, blank=False, default='2000-01-01')

    waktu_tanggal = models.TimeField(null=False, blank=False, default='09:01')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.perusahaan

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class ReviewUser (models.Model):

    class ReviewObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    # inisial tabel
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(
        _('Image'), upload_to=upload_reviews, null=True, blank=True)
    jabatan = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()  # The default manager.
    ReviewObjects = ReviewObjects()  # The custom manager.

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
