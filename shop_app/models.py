from django.db import models
from django.utils import timezone


class Product(models.Model):
    title = models.CharField("Title", max_length=250)
    price = models.IntegerField()
    qty = models.IntegerField(default=0)
    company = models.ForeignKey('shop_app.Company', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.company}"

    class Meta:
        verbose_name_plural = "Products"
        verbose_name = "product"


class Company(models.Model):
    title = models.CharField("Company title", max_length=250)
    phone = models.CharField("Company phone", max_length=50)
    address = models.CharField("Company address", max_length=250)

    def __str__(self):
        return self.title

    def products_type(self):
        return self.product_set.count()


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Sale(models.Model):
    customer = models.ForeignKey('shop_app.Customer', on_delete=models.CASCADE)
    product = models.ForeignKey('shop_app.Product', on_delete=models.CASCADE)
    company = models.ForeignKey('shop_app.Company', on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.product.company != self.company:
            raise ValueError('Selected product does not belong to the selected company.')

        if self.product.qty >= self.quantity_sold:
            self.product.qty -= self.quantity_sold
            self.product.save()
            super().save(*args, **kwargs)
        else:
            raise ValueError('Mahsulot soni yetarli emas!')

    def __str__(self):
        return f'{self.customer.name} - {self.product.title} - {self.quantity_sold}'