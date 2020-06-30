from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    Product_TYPES = [
        ('E', 'Electric'),  # Wert und lesbare Form
        ('G', 'Games'),
        ('B', 'books'),
        ('O', 'Other'),
    ]

    title = models.CharField(max_length=100)
    Desc = models.CharField(max_length=100,
                                blank=True)

    date_published = models.DateField(blank=True,
                                      default=date.today,
                                      )
    type = models.CharField(max_length=1,
                            choices=Product_TYPES,
                            )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='users',
                             related_query_name='user',
                             )
    Img = models.ImageField(upload_to='products/',blank=True)

    class Meta:
        ordering = ['title', '-type']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def get_full_title(self):
        return_string = self.title
        if self.Desc:  # if subtitle is not empty
            return_string = self.title + ': ' + self.Desc
        return return_string

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.get_full_title() + ' / ' + self.type
