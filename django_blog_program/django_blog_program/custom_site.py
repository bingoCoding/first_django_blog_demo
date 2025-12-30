from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'Blog博客'
    site_title = 'Blog博客管理'
    index_title = '首页'

custom_site = CustomSite(name='cus_admin')
