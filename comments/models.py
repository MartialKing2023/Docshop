from django.db import models
from store.models import Product
from shop.settings import AUTH_USER_MODEL

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, related_name='commentaires', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    parent_id = models.ForeignKey('self', null=True, blank=True, related_name='reponses', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Commentaire de {self.user} sur {self.product}"