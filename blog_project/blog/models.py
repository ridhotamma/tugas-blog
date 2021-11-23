from django.db import models
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from django.contrib.auth.models import User

class Writer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=180, null=True, blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/' % self.slug

class Post(models.Model):
    ACTIVE = 'active'
    DRAFT = 'draft'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft')
    )

    RECOMMENDED = 'Recommended'
    DEFAULT = 'default'

    CHOICES_PRIORITY = (
        (RECOMMENDED, 'Recommended'),
        (DEFAULT, 'Default')
    )
    writer = models.ForeignKey(Writer, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=180, null=True, blank=True)
    intro = models.TextField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=ACTIVE)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True, default="https://cdn.pixabay.com/photo/2021/08/25/20/42/field-6574455__480.jpg")
    priority = models.CharField(choices=CHOICES_PRIORITY, max_length=28, default=DEFAULT)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Category)
pre_save.connect(slug_generator, sender=Post)