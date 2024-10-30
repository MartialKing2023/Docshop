from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

# Create your views here.
from store.models import Product, Cart, Order
from comments.models import Comment


def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', context={"products": products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    # Creer un commentaire
    if request.method == "POST":
        content = request.POST.get("content")
        comment = Comment.objects.create(product=product,
                                         user=request.user,
                                         content=content)
        return redirect(reverse("product", kwargs={"slug": slug}))
    
    # Recuperer uniquement trois commentaires principaux les plus recents associe au produit
    comments = product.commentaires.filter(parent_id=None).order_by('-created_at')[0:3]
    return render(request, 'store/detail.html', context={"product": product, "comments": comments})


def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)  # La methode get_or_create
    # renvoit deux parametres et le "_" c'est pour specifie que le 2e parametre ne sera pas utilise
    order, created = Order.objects.get_or_create(user=user,
                                                 ordered=False, # Ligne ajoutee apres la surcharge de 'delete()'
                                                 product=product)
    
    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1  # Et si l'order a une quantite > 1 ????
        order.save()
        
    return redirect(reverse("product", kwargs={"slug": slug}))


def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    return render(request, 'store/cart.html', context={"orders": cart.orders.all()})


def cart_quantity_update():
    pass


# La methode delete ici a ete surcharge dans la classe Cart du fichier 'models.py'
def delete_cart(request):
    # 1ere facon d'ecrire
    cart = request.user.cart
    if cart:
        # cart.orders.all().delete() # La ligne ci ne sert plus a rien
        # puisque toute la logique a ete faite dans la classe Cart
        cart.delete()
        
    # 2e facon d'ecrire
    """if cart := request.user.cart:
        # cart.orders.all().delete() # Celle-ci aussi
        cart.delete()"""
        
    return redirect('index')