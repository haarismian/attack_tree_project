from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_node/', views.create_node, name='create_node'),
    path('get_tree/', views.get_tree, name='get_tree'),
    path('sum_route/', views.sum_route, name='sum_route'),
    path('export_tree/', views.export_tree, name='export_tree'),
    path('import_tree/', views.import_tree, name='import_tree'),
]
