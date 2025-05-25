"""
URL configuration for config project.

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
from django.urls import path, include
from ledger import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('export/', views.export_csv, name='export_csv'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('guest_login/', views.guest_login, name='guest_login'),
]

# ✅ これを urlpatterns の下に追記（順番大事）
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ← このすぐ下に追加！
urlpatterns += [
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
]
urlpatterns += [
    path('about/', views.about, name='about'),
]
