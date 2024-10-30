from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from store.models import Product
from comments.models import Comment

# Create your views here.
def index(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    # Creer un commentaire
    if request.method == "POST":
        content = request.POST.get("content")
        comment = Comment.objects.create(product=product,
                                         user=request.user,
                                         content=content)
        return redirect(reverse("comment-index", kwargs={"slug": slug}))
    comments = product.commentaires.filter(parent_id=None).order_by("-created_at")
    
    return render(request, 'comments/index.html', context={"product":product,
                                                           "comments":comments})


def reponse(request, id):
    comment = get_object_or_404(Comment, id=id)
    
    # Repondre au commentaire
    if request.method == "POST":
        content = request.POST.get("content")
        reponse = Comment.objects.create(product=comment.product,
                                         user=request.user,
                                         content=content,
                                         parent_id = comment)
        return redirect(reverse("comment-index", kwargs={"slug": reponse.product.slug}))
    
    return render(request, 'comments/reponse.html', context={"comment": comment})