from django.contrib import admin
from django.urls import path, include
from ledger import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('export/', views.export_csv, name='export_csv'),
    path('accounts/', include('django.contrib.auth.urls')),  # 👈 認証機能を追加
    path('accounts/signup/', views.signup, name='signup'),
]
