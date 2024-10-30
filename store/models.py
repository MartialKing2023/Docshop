from django.db import models
from django.urls import reverse
from django.utils import timezone

from shop.settings import AUTH_USER_MODEL

# Create your models here.
'''
Product
- Nom
- Prix
- La quantite en stock
- Description
- Image
'''


class Product(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="products", blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product', kwargs={"slug": self.slug})
    
    
# Article (Order)
"""
- Utilisateur
- Produit
- Quantite
- Commande ou non
"""
class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
    def get_prix_total(self):
        return self.product.price * self.quantity


# Panier (Cart)
"""
- Utilisateur
- Articles
- Commande ou non
- Date de la commande
"""

class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    
    def __str__(self):
        return self.user.username
    
    def get_total_prix(self):
        total = sum(order.get_prix_total() for order in self.orders.all())
        return total
    
    # Pour qu'en supprimant a partir de l'interface d'administration ou d'un
    # shell, on ait les memes effets. On va surcharger la methode 'delete' de django
    def delete(self, *args, **kwargs): # *args=arguments positionnels, **kwargs=arguments nommes
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
            
        self.orders.clear() # Pour que les articles ne soient plus lies au panier
        super().delete(*args, **kwargs)