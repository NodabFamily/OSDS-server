from ast import BinOp
from django.shortcuts import render,get_object_or_404
from django.views.decorators.http import require_http_methods
import json
import bcrypt

from django.http import JsonResponse, HttpResponse
from accounts.models import User
from .models import Family

# Create your views here.
@require_http_methods(['POST'])
def create_family(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))

        sender = request.user

        password = body['password']
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),bcrypt.gensalt()
        )
        decoded_password = hashed_password.decode('utf_8')

        new_family = Family.objects.create(
            family_name = body['family_name'],
            cover_image = body['cover_image'],
            bio = body['bio'],
            password = decoded_password
        )

        sender.is_participant = True
        sender.family_id = new_family
        sender.save()

        new_family_json = {
            "id" : new_family.id,
            "family_name" : new_family.family_name,
            "cover_image" : new_family.cover_image,
            "bio" : new_family.bio,
            "password" : new_family.password,
            "created_at" : new_family.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            "updated_at" : new_family.updated_at.strftime("%m/%d/%Y, %H:%M:%S")
        }

        json_res = json.dumps(
            {
            "status": 200,
            "success": True,
            "message": "생성 성공!",
            "data": new_family_json
            },
        ensure_ascii=False
        )

        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )


@require_http_methods(['GET','PATCH'])
def check_validate_family(request,family_id):
    # 가입하려는 가족 그롭이 이 가족이 맞는지 보여주는 코드
    if request.method == 'GET':
        family = get_object_or_404(Family, pk=family_id)
        member_json_all = []
        member_all = User.objects.filter(family_id = family)
        
        for member in member_all : 
            member_json = {
                "name" : member.name,
                "nickname" : member.nickname,
                "bio" : member.bio
            }
            member_json_all.append(member_json)

        family_json = {
            "family_name" : family.family_name,
            "cover_image" : family.cover_image,
            "bio" : family.bio,
            "members" : member_json_all
        }
        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "조회 성공",
                "data": family_json
            },
            ensure_ascii=False
        )
            
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

    # 입력한 패스워드와 가족 패스워드가 일치한지 확인해서 가입시키는 코드
    elif request.method == 'PATCH':
        body = json.loads(request.body.decode('utf-8'))

        rcvr = request.user

        pw_input = body['password']
        family = get_object_or_404(Family, pk=family_id)

        family_pw = family.password

        if bcrypt.checkpw(pw_input.encode('utf-8'), family_pw.encode('utf-8')) == True:
            rcvr.family_id = family
            rcvr.is_participant = True
            rcvr.save()

            json_res = json.dumps(
                {
                "status": 200,
                "success": True,
                "message": "생성 성공!",
                "data": None
                },
            ensure_ascii=False
            )
            
            return HttpResponse(
                json_res,
                content_type=u"application/json; charset=utf-8",
                status=200
            )

        else:
            json_res = json.dumps(
                {
                "status": 400,
                "success": False,
                "message": "비밀번호 불일치",
                "data": None
                },
            ensure_ascii=False
            )
            
            return HttpResponse(
                json_res,
                content_type=u"application/json; charset=utf-8",
                status=400
            )


@require_http_methods(['GET','PUT','DELETE'])
def read_update_delete_family(request,family_id):
    # 가족 정보 조회
    if request.method == 'GET':
        family = get_object_or_404(Family, pk=family_id)
        member_json_all = []
        member_all = User.objects.filter(family_id = family)
        
        for member in member_all : 
            member_json = {
                "name" : member.name,
                "nickname" : member.nickname,
                "bio" : member.bio
            }
            member_json_all.append(member_json)

        family_json = {
            "family_name" : family.family_name,
            "cover_image" : family.cover_image,
            "bio"         : family.bio,
            "members"     : member_json_all
        }
        
        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "조회 성공",
                "data": family_json
            },
            ensure_ascii=False
        )
            
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )
    
    # 가족 정보 수정
    elif request.method == 'PUT':
        body = json.loads(request.body.decode('UTF-8'))

        password = body['password']
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),bcrypt.gensalt()
        )
        decoded_password = hashed_password.decode('utf_8')

        update_family = get_object_or_404(Family, pk=family_id)
        update_family.family_name = body['family_name']
        update_family.cover_image = body['cover_image']
        update_family.bio = body['bio']
        update_family.password = decoded_password
        update_family.save()

        update_family_json = {
            "family_name" : update_family.family_name,
            "cover_image" : update_family.cover_image,
            "bio"         : update_family.bio,
            "password"    : update_family.password
        }

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "수정 성공",
                "data": update_family_json
            },
            ensure_ascii=False
        )
            
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

    # 가족 삭제
    elif request.method == 'DELETE':
        delete_family = get_object_or_404(Family, pk=family_id)
        delete_family.delete()
        
        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "삭제 성공",
                "data": None
            },
            ensure_ascii=False
        )
        
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

