from django.db import models


class DNSRecord(models.Model):
    ip_address = models.CharField(max_length=45)  # Supports IPv4 and IPv6
    domain = models.CharField(max_length=255)
