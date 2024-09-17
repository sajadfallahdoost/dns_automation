from django.urls import path
from cloudflare_dns.api.view import update_dns_record

urlpatterns = [
    path('update-dns/', update_dns_record, name='update_dns'),
]
