from django.db import models
from django.contrib.postgres.fields import ArrayField
#from autoslug import AutoSlugField
from task.helper import unique_slug_generator_name_category, youtube_url_validation
import task.repositories as repo
import task.models as m
from django.contrib import messages 

class Category(models.Model):
    def __str__(self):
        return self.name  
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank = True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = unique_slug_generator_name_category(self, category = False)
            self.save()

class Subcategory(models.Model):
    def __str__(self):
        return self.name  
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super(Subcategory, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = unique_slug_generator_name_category(self)
            self.save()

class Product(models.Model):
    def __str__(self):
        ret_val = str(self.name + ", "+ self.slug)
        return self.name

    name = models.TextField(max_length=255)
    slug = models.SlugField(unique=True, blank = True)
    main_image = models.ImageField(upload_to = 'static/images/', blank = True, null = True)
    description = models.TextField(max_length=255)
    inner_number = models.CharField(max_length=6)
    maker = models.CharField(max_length=255, blank = True)
    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    METRIC_CHOICES = (
        ('kg', 'kilogramms'),
        ('g', 'gramms'),
        ('L', 'litres'),
        ('ml', 'milliliters')
    )
    merics = models.CharField(max_length=2, choices=METRIC_CHOICES)
    old_price = models.DecimalField(max_digits = 20, decimal_places=2)
    promo_price = models.DecimalField(max_digits = 20, decimal_places=2, blank = True, null = True)
    quantity = models.DecimalField(max_digits = 20, decimal_places=2)
    #characteristics=
    new_marks = models.BooleanField(default=True)
    video = models.TextField(max_length=255, blank = True)
    weight_kg = models.DecimalField(max_digits = 20, decimal_places=2)
    meta_description = models.TextField()
    meta_words = ArrayField(models.CharField(max_length=20))
    meta_title = models.TextField(max_length=255)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        can_save = True
        if not self.slug:
            self.slug = unique_slug_generator_name_category(self)
            self.save()
        if self.video:
            if not youtube_url_validation(self.video):
                can_save = False
        if can_save:
            super(Product, self).save(*args, **kwargs)
            
class PostImage(models.Model):

    def __str__(self):
        ret_val = str(self.product) + ", "+ str(self.images)
        return ret_val

    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to = 'uploads/')

class PostDocument(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    doc = models.FileField(upload_to = 'uploads/documents/')

class ConnectedProducts(models.Model): 
    def __str__(self):
        ret_val = str(self.first_product) + ", "+ str(self.second_product)
        return ret_val

    first_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_one')
    second_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_two')
    are_purchased_together = models.BooleanField(default=False)
    are_connected = models.BooleanField(default=False)

    class Meta:
        unique_together = ('first_product', 'second_product')

    def save(self, *args, **kwargs):  
        cpRepo = repo.ConnectedProductsRepository(m.ConnectedProducts)
        is_exists = cpRepo.get_by_two_ids_combination(self.first_product, self.second_product)
        compare = str(self.first_product) + ", "+ str(self.second_product)
        if is_exists.count == 0 or str(is_exists[0]) == compare:
            super(ConnectedProducts, self).save(*args, **kwargs)
            

    






