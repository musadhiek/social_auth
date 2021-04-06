from django.urls import path
from account import views

urlpatterns =[
    path('',views.login,name='login'),
    path('sign_up',views.sign_up,name='sign_up'),
    path('log_out',views.log_out,name='log_out'),
    path('admin_login',views.admin_login,name='admin_login'),

    
    path('send_otp',views.send_otp,name='send_otp'),
    path('enter_otp',views.enter_otp,name='enter_otp'),
    
    path('user_page',views.user_page,name='user_page'),
    path('list_user',views.list_user,name='list_user'),
    path('delete_user',views.delete_user,name='delete_user'),
    path('block_user',views.block_user,name='block_user'),
    path('unblock_user',views.unblock_user,name='unblock_user'),

]
