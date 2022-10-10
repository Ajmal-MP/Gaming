from django.urls import path
from .views import *
urlpatterns = [
    path("admin_login",Admin_login,name='admin_login'),
    path("logout",Admin_logout,name='admin_logout'),
    path("user_display",user_display,name='user_display'),
    path("user_block/<int:id>/<int:flag>",user_block,name='user_block'),
    path("sales_report",sales_report,name='sales_report'),
    path("dashbord",dashbord,name='dashbord'),
    path("sales_report_month/<int:id>",sales_report_month,name='sales_report_month')
]