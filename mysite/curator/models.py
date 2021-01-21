from django.db import models

# Year shouldn't be in foreign key or in chained lists, as users may want to search in range of years
# class Year(models.Model):
#     year = models.IntegerField()

#     def __str__(self):
#         return str(self.year)

class Brand(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name




# # Create your models here.
class Ad(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    # year = models.ForeignKey(Year, on_delete=models.CASCADE)  # deprecated
    year = model.CharField(max_length=200)
    gov = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    date = models.DateField()  
    kilos = models.CharField(max_length=200)
    pay_type = models.CharField(max_length=200)
    transmission = models.CharField(max_length=200)
    cc = models.CharField(max_length=200, blank=True, null=True)
    chasis = models.CharField(max_length=200, blank=True, null=True)
    features = models.CharField(max_length=500, blank=True, null=True)
    color = models.CharField(max_length=200, blank=True, null=True)
    price = models.IntegerField()
    url = models.URLField()
    description = models.CharField(max_length=500, blank=True, null=True)
    imgs = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.brand,
                                    self.model,
                                    self.year)



    
