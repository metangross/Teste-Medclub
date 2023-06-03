from django.urls import path, re_path
from api.views.item import ItemView, ItemListView

urlpatterns = [
    re_path(r'^item/(?P<pk>[^\/])$', ItemView.as_view(), name='item-view'),
    re_path(r'^itemlist/$', ItemListView.as_view(), name='item-list-view'),
]