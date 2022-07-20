from django.urls import path
from . import views

app_name = 'urls'

urlpatterns = [
    path('', views.create, name = 'create'),

    path('login',views.loginn,name='login'),
    path('logout',views.logoutt,name='logout'),

    path('view',views.view,name = 'view'),
    path('edit/<int:idd>',views.edit,name='edit'),
    path('update/<int:idd>',views.update,name = 'update'),
    path('delete/<int:idd>',views.delete,name ='delete'),

    path('receive',views.receive_js,name="receive"),
    
    path('csv',views.export,name ='csv'),
    path('nuke',views.nuke,name='nuke'),

    path('<str:token>', views.redirector, name = 'redirect')
]
