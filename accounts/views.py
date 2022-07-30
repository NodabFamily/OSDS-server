from unicodedata import category
from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import User
from django.views.decorators.http import require_http_methods
# Create your views here.
# 내일 해결해야할 것들  : family_id  ,, 사진 불러오고 수정하기 
@require_http_methods(['POST'])
def create_user(request):
    if request.method == "POST":
        body = request.POST
        avatar_img = request.FILES['avatar']

        new_user =  User.objects.create(
            #family_id = body["family_id"],
            member_id = body["member_id"],
            password = body["password"],
            name = body["name"],
            birth = body["birth"],
            bio = body["bio"],
            is_participant = body["is_participant"],
            avatar = avatar_img,
            nickname = body["nickname"],    
        )

        new_user_json={
            "id"    : new_user.id,
            #"family_id" : new_user.family_id.id,
            "password" : new_user.password,
            "member_id" : new_user.member_id,
            "name"    : new_user.name,
            "birth"    : new_user.birth,
            "bio"    : new_user.bio,
            "avatar"    : new_user.avatar.url,
            "nickname"    : new_user.nickname,
            "is_participant"    : new_user.is_participant,

        }

        return JsonResponse({
                    'status': 200,
                    'success': True,
                    'message': '생성 성공!',
                    'data': new_user_json    
                })


@require_http_methods(['GET','DELETE','PUT'])
def read_edit_delete_user(request,id):
    if request.method == "GET":
        user_detail = get_object_or_404(User, pk =id)
        user_detail_json={
            "id"   : user_detail.id,
            "password" : user_detail.password,
            "member_id" : user_detail.member_id,
            "name"    : user_detail.name,
            "birth"    : user_detail.birth,
            "bio"    : user_detail.bio,
            "avatar"    : user_detail.avatar.url,
            "nickname"    : user_detail.nickname,
            "is_participant"    : user_detail.is_participant,
        }

        return JsonResponse({
                'status': 200,
                'success': True,
                'message': '수신 성공!',
                'data': user_detail_json
            })

    elif request.method == "DELETE":
        delete_user = get_object_or_404(User, pk=id)
        delete_user.delete()
        return JsonResponse({
                'status': 200,
                'success': True,
                'message': '삭제 성공!',
                'data': None
            })

    elif request.method == "PUT":
        body = json.loads(request.body.decode('utf8'))
        #avatar_img = request.FILES['avatar']
        

        update_user = get_object_or_404(User, pk =id)
        update_user.member_id = body["member_id"]
        update_user.password = body["password"]
        update_user.name = body["name"]
        update_user.birth = body["birth"]
        update_user.bio = body["bio"]
        #update_user.avatar = avatar_img
        update_user.nickname = body["nickname"]

        update_user.save()

        update_user_json={
            "id"    : update_user.id,
            #"family_id" : new_user.family_id.id,
            "password" : update_user.password,
            "member_id" : update_user.member_id,
            "name"    : update_user.name,
            "birth"    : update_user.birth,
            "bio"    : update_user.bio,
            #"avatar"    : update_user.avatar.url,
            "nickname"    : update_user.nickname,
        }

        return JsonResponse({
                'status': 200,
                'success': True,
                'message': '업데이트 성공!',
                'data': update_user_json
            })