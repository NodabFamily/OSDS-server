import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from accounts.models import Family
from .models import Album
# Create your views here.


def create_album(request, family_id):
    if request.method == "POST":

        body = request.POST
        img = request.FILES['cover_image']

        new_album = Album.objects.create(
            family_id=get_object_or_404(Family, pk=family_id),
            title=body["title"],
            cover_image=img
        )

        new_album_json = {
            "id": new_album.id,
            "title": new_album.title,
            "family_id": new_album.family_id.id,
            "cover_image": new_album.get_img_url(),
            "created_at": new_album.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            "updated_at": new_album.updated_at.strftime("%m/%d/%Y, %H:%M:%S"),

        }
        json_res = json.dumps(
            {
            "status": 200,
            "success": True,
            "message": "생성 성공!",
            "data": new_album_json
            },
        ensure_ascii=False
        )

        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

    return JsonResponse({
        'status': 405,
        'success': False,
        'message': 'method error',
        'data': None
    })