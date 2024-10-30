from django.urls import path
from comments.views import index, reponse


urlpatterns = [
    path('<str:slug>/', index, name="comment-index"),
    path('reponse/<int:id>/', reponse, name="comment-reponse"),
]
