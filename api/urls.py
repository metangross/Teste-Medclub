from django.urls import re_path

from api.views.item import ItemListView, ItemView
from api.views.pedido import PedidoUserView, PedidoView
from api.views.user import LoginView, UserListView, UserView

urlpatterns = [
    re_path(r"^item/(?P<pk>\d+)$", ItemView.as_view(), name="item-view"),
    re_path(r"^item/$", ItemListView.as_view(), name="item-list-view"),
    re_path(r"^pedido/$", PedidoView.as_view(), name="pedido-view"),
    re_path(
        r"^pedido/(?P<pk>\d+)$$", PedidoUserView.as_view(), name="item-pedido-view"
    ),
    re_path(r"^user/$", UserView.as_view(), name="user-view"),
    re_path(r"^newuser/$", UserListView.as_view(), name="user-list-view"),
    re_path(r"^auth/$", LoginView.as_view(), name="login-view"),
]
