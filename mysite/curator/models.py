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
    cc = models.CharField(max_length=200)
    chasis = models.CharField(max_length=200)
    features = models.CharField(max_length=500)
    color = models.CharField(max_length=200)
    price = models.IntegerField()
    url = models.URLField()

    def __str__(self):
        return '{} - {} - {}'.format(self.brand,
                                    self.model,
                                    self.year)
    
