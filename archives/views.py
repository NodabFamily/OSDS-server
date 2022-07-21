from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import json
# Create your views here.

from accounts.models import Family
from archives.models import Album


def create_album(requests, family_id):
    if requests.method == "POST":
        body = requests.body.decode('utf-8')
        img = requests.FILES['cover_image']

        new_album = Album.objects.create(
            family_id=get_object_or_404(Family, pk=family_id),
            title=body['title'],
            cover_image=img
        )

        new_album_json = {
            "id": new_album.id,
            "family_id": new_album.family_id,
            "title": new_album.title,
            "cover_image": new_album.cover_image,
            "created_at": new_album.created_at,
            "updated_at": new_album.updated_at,
        }

        return JsonResponse({
            'status': 200,
            'success': True,
            'message': '생성 성공!',
            'data': new_album_json
        })

    return JsonResponse({
        'status': 405,
        'success': False,
        'message': 'method error',
        'data': None
    })