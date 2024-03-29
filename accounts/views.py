import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
# Create your views here.
User = get_user_model()

@require_http_methods(['POST'])
def create_user(request):
    body = json.loads(request.body.decode('utf-8'))
    new_user =  User.objects.create(
            username = body["username"],
            password = body["password"],
            name = body["name"],
            birth = body["birth"],
            bio = body["bio"],
            is_participant = body["is_participant"],
            avatar = body["avatar"],
            nickname = body["nickname"]   
        )
    new_user.password = make_password(body["password"])
    new_user.save()

    new_user_json={
            "id"    : new_user.id,
            "username" : new_user.username,
            "name"    : new_user.name,
            "birth"    : new_user.birth,
            "bio"    : new_user.bio,
            "avatar"    : new_user.avatar,
            "nickname"    : new_user.nickname,
            "is_participant"    : new_user.is_participant
        }

    

    json_res=json.dumps(
                {
                'status': 200,
                'success': True,
                'message': '생성 성공!',
                'data': new_user_json    
                },
            ensure_ascii=False
            )
    return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )

@require_http_methods(['POST'])
def login_view(request):
    print("request.user : ", request.user)
    print("request.POST : ", request.POST.get("username"))
    print("request.body : ", request.body)
    data = json.loads(request.body.decode("utf-8"))
    print("data : ", data)             

    username = data['username']
    password = data['password']

    print(username)
    print(password)
    user = authenticate(request, username=username , password = password)

    if user is not None:
        login(request, user)
        user_data = {
                "id"   : user.id,
                "username" : user.username,
                "name"    : user.name,
                "birth": user.birth,
                "bio":user.bio,
                "nickname":user.nickname,
                "is_participant":user.is_participant
            }
        return JsonResponse({"success": True, "message" : "로그인 성공", "data" : user_data}, status = 200)
    else: 
        return JsonResponse({"success": False, "message": "로그인 실패"}, status = 403)
   


@require_http_methods(['POST'])
def logout_view(request): 
    logout(request)

    return JsonResponse({
        "success": True,
        "message": "로그아웃 성공"},
        status = 200)


@require_http_methods(['GET','DELETE','PUT'])
def read_edit_delete_user(request,id):
    if request.method == "GET":
        user_detail = get_object_or_404(User, pk =id)
        user_detail_json={
            "id"   : user_detail.id,
            "username" : user_detail.username,
            "name"    : user_detail.name,
            "birth"    : user_detail.birth,
            "bio"    : user_detail.bio,
            "avatar"    : user_detail.avatar,
            "nickname"    : user_detail.nickname,
            "is_participant"    : user_detail.is_participant
        }
        json_res = json.dumps(
                {
                "status": 200,
                "success": True,
                "message": "조희 성공!",
                "data": user_detail_json
                },
            ensure_ascii=False
            )
            
        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        )
    elif request.method == "DELETE":
        delete_user = get_object_or_404(User, pk=id)
        delete_user.delete()
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

    elif request.method == "PUT":
        body = json.loads(request.body.decode('utf-8'))

        update_user = get_object_or_404(User, pk =id)
        update_user.username = body["username"]
        update_user.name = body["name"]
        update_user.birth = body["birth"]
        update_user.bio = body["bio"]
        update_user.avatar = body["avatar"]
        update_user.nickname = body["nickname"]

        update_user.save()

        update_user_json={
            "id"    : update_user.id,
            "username" : update_user.username,
            "name"    : update_user.name,
            "birth"    : update_user.birth,
            "bio"    : update_user.bio,
            "avatar"    : update_user.avatar,
            "nickname"    : update_user.nickname,
        }

        json_res = json.dumps(
            {
                "status": 200,
                "success": True,
                "message": "수정 성공",
                "data": update_user_json
            },
            ensure_ascii=False
        )

        return HttpResponse(
            json_res,
            content_type=u"application/json; charset=utf-8",
            status=200
        ) 