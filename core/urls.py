"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from core.views import crm_view, dashboard_view, finance_view, hr_view, module_page_view, projects_view, reports_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('crm/', crm_view, name='crm'),
    path('finance/', finance_view, name='finance'),
    path('hr/', hr_view, name='hr'),
    path('projects/', projects_view, name='projects'),
    path('reports/', reports_view, name='reports'),
    path('modules/<slug:module_slug>/', module_page_view, name='module_page'),
    path('api/', include(('erp_modules.urls', 'erp_modules'), namespace='erp_modules')),
    path('auth/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('admin/', admin.site.urls),
]
