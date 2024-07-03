from django.db import models
from django.core import validators
from members.models import Member
from django.utils.translation import gettext as _
from django.utils import timezone


class Storage(models.Model):
    name = models.CharField(max_length=100)
    stock = models.IntegerField(default=0, validators=[validators.MinValueValidator(0)])
    def __str__(self):
        return self.name
    
  
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('hot_drinks', 'نوشیدنی گرم'),
        ('cold_drinks', 'نوشیدنی سرد'),
        ('cakes', 'کیک'),
    ]
    
    category = models.CharField(_("دسته بندی محصول"),max_length=20, choices=CATEGORY_CHOICES, default='hot_drinks')
    name = models.CharField(_('نام'), max_length=255)
    description = models.CharField( _("توضیحات"), max_length=255, blank=True, null=True)
    price = models.DecimalField(_("قیمت"),default=0, max_digits=10, decimal_places=2, validators=[validators.MinValueValidator(0)])
    timeNeeded = models.IntegerField(_("زمان مورد نیاز"),default=0, validators=[validators.MaxValueValidator(60)])
    coffee = models.PositiveIntegerField(_("قهوه"),default=0)
    milk = models.PositiveIntegerField(_("شیر"),default=0)
    chocolate = models.PositiveIntegerField(_("شکلات"),default=0)
    flour = models.PositiveIntegerField(_("آرد"),default=0)
    sugar = models.PositiveIntegerField(_("شکر"),default=0)
    image = models.ImageField(_("تصویر"),upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # raw_materials = models.ManyToManyField(Storage, through='ProductStorage')
    # vertical = models.BinaryField(auto_created=True, unique=True, blank=True, null=True)
    sold_count = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.name


class ProductStorage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    raw_materials = models.ForeignKey(Storage, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.raw_materials.name} for {self.product.name}"


class Order(models.Model):
    customer = models.ForeignKey(Member, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')
    order_date = models.DateTimeField(default=timezone.now)
    Type = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return str(self.pk)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[validators.MinValueValidator(1)])

    def __str__(self) -> str:
        return f"{self.quantity} of {self.product.name} for {self.order.customer}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_storage()

    def update_storage(self):
        product = self.product
        material_quantities = {
            'قهوه': 0,
            'شیر': 0,
            'شکلات': 0,
            'آرد': 0,
            'شکر': 0,
        }
        material_quantities['قهوه'] += product.coffee * self.quantity
        material_quantities['شیر'] += product.milk * self.quantity
        material_quantities['شکلات'] += product.chocolate * self.quantity
        material_quantities['آرد'] += product.flour * self.quantity
        material_quantities['شکر'] += product.sugar * self.quantity

        for material, quantity in material_quantities.items():
            storage = Storage.objects.get(name=material)
            storage.stock -= quantity
            storage.save()    


class CustomerOrder(models.Model):
    customer = models.ForeignKey(Member, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.pk)
    
