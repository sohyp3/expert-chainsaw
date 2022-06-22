from django.urls import path
from . import views

app_name = 'urls'

urlpatterns = [
    path('', views.create, name = 'create'),

    path('view',views.view,name = 'view'),
    path('view2',views.search,name='search'),
    path('edit/<int:idd>',views.edit,name='edit'),
    path('update/<int:idd>',views.update,name = 'update'),
    path('delete/<int:idd>',views.delete,name ='delete'),

    path('receive',views.receive_js,name="receive"),

    path('<str:token>', views.redirector, name = 'redirect')
]
