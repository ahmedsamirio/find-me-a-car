from django.db import models

# Create your models here.
class Ad(models.Model):
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    gov = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    date = models.DateField()  
    year = models.IntegerField()
    kilos = models.CharField(max_length=200)
    pay_type = models.CharField(max_length=200)
    transmission = models.CharField(max_length=200)
    cc = models.CharField(max_length=200, blank=True, null=True)
    chasis = models.CharField(max_length=200, blank=True, null=True)
    features = models.CharField(max_length=500, blank=True, null=True)
    color = models.CharField(max_length=200, blank=True, null=True)
    price = models.IntegerField()
    url = models.URLField()
    description = models.CharField(max_length=2000, blank=True, null=True)
    imgs = model.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.brand,
                                    self.model,
                                    self.year)
    
