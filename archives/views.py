import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from accounts.models import Family
from .models import Album, Like, Photo

from django.views.decorators.http import require_http_methods
# Create your views here.

@require_http_methods(['POST', 'GET'])
def create_read_all_album(request, family_id):
    if request.method == "POST":

        body = request.POST
        img = request.FILES['album_image']

        new_album = Album.objects.create(
            family_id=get_object_or_404(Family, pk=family_id),
            title=body["title"],
            cover_image=img
        )

        new_album_json = {
            "id": new_album.id,
            "title": new_album.title,
            "family_id": new_album.family_id.id,
            "cover_image": new_album.album_image.url,
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

    elif request.method == "GET":
        # 변수 초기화
        like_count = 0
        comment_count = 0

        user = request.user.family_id

        album_all = Album.objects.filter(family_id=user)
        album_json_all = []

        for album in album_all:
            photo_all = Photo.objects.filter(album_id=album.id)

            for photo in photo_all:

                like_count += photo.like_set.all().count()
                comment_count += photo.comment_set.all().count()

            album_json = {
                "id" : album.id,
                "family_id" : user,
                "title" : album.title,
                "album_image" : album.album_image.url,
                "like_count" : like_count,
                "comment_count" : comment_count,
                "created_at" : album.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
                "updated_at" : album.updated_at.strftime("%m/%d/%Y, %H:%M:%S")
            }
            print(album_json)
            album_json_all.append(album_json)
            like_count = 0
            comment_count = 0
        print(album_json_all)
        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "생성 성공!",
                "data": album_json_all
            },
            ensure_ascii=False
        )

        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )


@require_http_methods(['GET', 'PUT', 'PATCH', 'DELETE'])
def read_edit_delete_album(request, family_id, album_id):
    if request.method == "GET":
        # 변수 초기화
        like_count = 0
        comment_count = 0
        photo_json_all = []

        user = family_id

        photo_all = Photo.objects.filter(album_id=album_id)
        for photo in photo_all:
            like_count = photo.like_set.all().count()
            comment_count = photo.comment_set.all().count()

            photo_json = {
                "id" : photo.id,
                "album_id" : photo.album_id.id,
                "family_id" : photo.family_id.id,
                "photo_image" : photo.photo_image.url,
                "like_count" : like_count,
                "comment_count" : comment_count,
                "created_at" : photo.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
                "updated_at" : photo.updated_at.strftime("%m/%d/%Y, %H:%M:%S")
            }
            photo_json_all.append(photo_json)

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "생성 성공!",
                "data": photo_json_all
            },
            ensure_ascii=False
        )

        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

    elif request.method == "PUT":
        pass
    elif request.method == "PATCH":
        pass
    elif request.method == "DELETE":
        pass