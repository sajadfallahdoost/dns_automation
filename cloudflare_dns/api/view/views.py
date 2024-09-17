import os
import requests
from kernel import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Helper function to add an A record to Cloudflare
def add_a_record_to_cloudflare(ip):
    url = f'https://api.cloudflare.com/client/v4/zones/{settings.CLOUDFLARE_ZONE_ID}/dns_records'
    headers = {
        'Authorization': f'Bearer {settings.CLOUDFLARE_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'type': 'A',
        'name': 'grafana.gundicut.com',  # Replace with your domain/subdomain
        'content': ip,
        'ttl': "Auto",  # Adjust TTL as needed
        'proxied': False,
    }

    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200


# Function-based view to handle POST request
@api_view(['POST'])
def update_dns_record(request):
    file_path = os.path.join('source/', 'ip.txt')

    try:
        with open(file_path, 'r') as file:
            ip_list = file.read().splitlines()

        for ip in ip_list:
            # breakpoint()
            # Add each IP to Cloudflare as an A record
            if not add_a_record_to_cloudflare(ip):
                return Response({'error': f'Failed to add A record for IP: {ip}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'DNS records updated successfully'}, status=status.HTTP_200_OK)

    except FileNotFoundError:
        return Response({'error': 'File not found'}, status=status.HTTP_400_BAD_REQUEST)
