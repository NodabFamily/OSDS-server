import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from families.models import Family
from .models.comment import Comment
from .models.photo import Photo
from .models.album import Album

from django.views.decorators.http import require_http_methods
# Create your views here.

@require_http_methods(['POST', 'GET'])
def create_read_all_album(request, family_id):
    if request.method == "POST":

        body = request.POST
        img = request.FILES.get('cover_image')
        album_img = request.FILES.getlist['album_image']

        new_album = Album.objects.create(
            family_id=get_object_or_404(Family, pk=family_id),
            title=body["title"],
            cover_image=img
        )

        for image in album_img:
            photo = Photo.objects.create(
                album_id=new_album.id,
                family_id=family_id.id,
                photo_image=image
            )
            photo.save()


        new_album_json = {
            "id": new_album.id,
            "title": new_album.title,
            "family_id": new_album.family_id.id,
            "album_image": new_album.album_image.url,
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
            album_json_all.append(album_json)
            like_count = 0
            comment_count = 0

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


@require_http_methods(['GET', 'PUT', 'DELETE'])
def read_edit_delete_album(request, family_id, album_id):
    if request.method == "GET":
        photo_json_all = []

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
        body = json.loads(request.body.decode('utf8'))
        # 앨범 타이틀 수정
        # album = Album.objects.get(id=album_id)
        album = get_object_or_404(Album, id=album_id)

        new_title = body['title']

        album.title = new_title
        album.save()

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "수정 성공!",
                "data": new_title
            },
            ensure_ascii=False
        )

        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )


    elif request.method == "DELETE":
        # 앨범 삭제
        album = Album.objects.get(id=album_id)
        album.delete()

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "삭제 성공!"
            },
            ensure_ascii=False
        )

        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

@require_http_methods(['DELETE'])
def delete_photo(request, family_id, album_id, photo_id):
    if request.method == 'DELETE':
        photo = get_object_or_404(Photo, pk=photo_id)
        photo.delete()

    json_res = json.dumps(
        {
            "status": 200,
            "success": True,
            "message": "삭제 성공!"
        },
        ensure_ascii=False
    )

    return HttpResponse(
        json_res,
        content_type=u"application/json; charset=utf-8",
        status=200
    )


@require_http_methods(['POST'])
def create_comment(request, family_id, photo_id):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf8'))
        user = request.user
        print(user)
        new_comment = Comment.objects.create(
            photo_id=get_object_or_404(Photo, pk=photo_id),
            user_id=user.id,
            comment=body['comment']
        )
        new_comment_json = {
            "id": new_comment.id,
            "photo_id": new_comment.photo_id.id,
            "user_id": new_comment.user_id,
            "comment": new_comment.comment,
            "created_at": new_comment.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            "updated_at": new_comment.updated_at.strftime("%m/%d/%Y, %H:%M:%S"),
        }
        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "생성 성공!",
                "data": new_comment_json
            },
            ensure_ascii=False
        )

        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

@require_http_methods(['PUT', 'DELETE'])
def edit_delete_comment(request, family_id, photo_id, comment_id):
    if request.method == "PUT":
        body = json.loads(request.body.decode('utf8'))
        comment = get_object_or_404(Comment, pk=comment_id)

        new_comment = body['comment']

        comment.comment = new_comment
        comment.save()

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "수정 성공!",
                "data": new_comment
            },
            ensure_ascii=False
        )

        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

    elif request.method == "DELETE":
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "삭제 성공!"
            },
            ensure_ascii=False
        )

        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

