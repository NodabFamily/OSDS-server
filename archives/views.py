import json

from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

from accounts.models import User
from families.models import Family
from .models import Like
from .models.bookmark import Bookmark
from .models.comment import Comment
from .models.photo import Photo
from .models.album import Album

from django.views.decorators.http import require_http_methods
# Create your views here.

@require_http_methods(['POST', 'GET'])
def create_read_all_album(request, family_id):
    if request.method == "POST":

        body = json.loads(request.body.decode('utf8'))
        album_img = body['album_image']
        user = request.user.id
        new_album = Album.objects.create(
            user_id=user,
            family_id=get_object_or_404(Family, pk=family_id),
            title=body.get("title"),
            cover_image=body.get("cover_image")
        )
        for image in album_img:
            photo = Photo.objects.create(
                user_id=user,
                album_id_id=new_album.id,
                family_id_id=family_id,
                photo_image=image
            )
            photo.save()


        new_album_json = {
            "id": new_album.id,
            "title": new_album.title,
            "user_id": new_album.user_id,
            "family_id": new_album.family_id.id,
            "cover_image": new_album.cover_image,
            "created_at": new_album.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            "updated_at": new_album.updated_at.strftime("%m/%d/%Y, %H:%M:%S")
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
        user = request.user

        album_all = Album.objects.order_by("-id").filter(family_id=family_id)
        album_json_all = []

        for album in album_all:
            photo_all = Photo.objects.order_by("-id").filter(album_id=album.id)
            for photo in photo_all:
                like_count += photo.like_count
                comment_count += photo.comment_set.all().count()

            album_json = {
                "id" : album.id,
                "family_id" : family_id,
                "title" : album.title,
                "user_id" : album.user_id.id,
                "album_image" : album.album_image,
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
        user_id = request.user.id
        photo_all = Photo.objects.filter(album_id=album_id).order_by("-id").prefetch_related(Prefetch("like_set", queryset=Like.objects.filter(user_id=user_id), to_attr="my_likes"), Prefetch("bookmark_set", queryset=Bookmark.objects.filter(user_id=user_id), to_attr="my_bookmarks"))
        for photo in photo_all:
            like_count = photo.like_set.all().count()
            comment_count = photo.comment_set.all().count()
            user_like = photo.my_likes
            user_bookmark = photo.my_bookmarks

            if user_like:
                my_like=1
            else:
                my_like=0

            if user_bookmark:
                my_bookmark=1
            else:
                my_bookmark=0

            photo_json = {
                "id" : photo.id,
                "album_id" : photo.album_id.id,
                "family_id" : photo.family_id.id,
                "user_id" : photo.user_id,
                "photo_image" : photo.photo_image,
                "like_count" : like_count,
                "comment_count" : comment_count,
                "created_at" : photo.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
                "updated_at" : photo.updated_at.strftime("%m/%d/%Y, %H:%M:%S"),
                "my_like" : my_like,
                "my_bookmark" : my_bookmark

            }
            photo_json_all.append(photo_json)

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "조회 성공!",
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


@require_http_methods(['POST', 'GET'])
def create_comment(request, family_id, photo_id):
    user = request.user
    if request.method == "POST":
        body = json.loads(request.body.decode('utf8'))
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

    elif request.method == 'GET':
        comment_all = Comment.objects.filter(photo_id=photo_id)
        comment_json_all = []
        for comment in comment_all:
            comment_json = {
                "photo_id" : comment.photo_id,
                "user_id" : comment.user_id,
                "comment" : comment.comment
            }
            comment_json_all.appned(comment_json)

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "조회 성공!",
                "data": comment_json_all
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


@require_http_methods(['POST', 'DELETE'])
def do_undo_like(request, family_id, album_id, photo_id):
    if request.method == "POST":
        user = request.user.id
        photo = get_object_or_404(Photo, pk=photo_id)

        photo.like_count += 1
        photo.save()
        photo_like = Like.objects.create(user_id=user, photo_id=photo)

        new_like_json = {
            "user_id" : user.id,
            "photo_id" : photo_id,
            "created_at" : photo_like.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
        }

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "생성 성공!",
                "data": new_like_json
            },
            ensure_ascii=False
        )

        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

    elif request.method == "DELETE":
        user = request.user.id
        deleted_cnt = Like.objects.filter(user_id=user, photo_id=photo_id)
        if deleted_cnt:
            photo = Photo.objects.filter(id=photo_id).get()
            photo.like_count -= 1
            photo.save()
            photo_like = Like.objects.filter(user_id=user, photo_id=photo_id)
            photo_like.delete()

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

@require_http_methods(['POST', 'DELETE'])
def do_undo_bookmark(request, family_id, album_id, photo_id):
    user = request.user.id
    photo = get_object_or_404(Photo, pk=photo_id)

    if request.method == "POST":

        bookmark_photo = Bookmark.objects.create(user_id=user, photo_id=photo)

        new_bookmark_json = {
            "user_id": user.id,
            "photo_id": photo_id,
            "created_at": bookmark_photo.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
        }

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "생성 성공!",
                "data": new_bookmark_json
            },
            ensure_ascii=False
        )

        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

    elif request.method == "DELETE":
        deleted_cnt = Bookmark.objects.filter(user_id=user, photo_id=photo_id)
        if deleted_cnt:
            bookmark_photo = Bookmark.objects.filter(user_id=user, photo_id=photo_id)
            bookmark_photo.delete()

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
