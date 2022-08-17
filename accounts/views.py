from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.signals import user_logged_out
from django.http import JsonResponse
# Create your views here.
@require_http_methods(['POST'])
def create_user(request):

    if request.method == "POST":
        body = request.POST
        avatar_img = request.FILES['avatar']
        new_user =  User.objects.create(
            username = body["username"],
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
            "password" : new_user.password,
            "username" : new_user.username,
            "name"    : new_user.name,
            "birth"    : new_user.birth,
            "bio"    : new_user.bio,
            "avatar"    : new_user.avatar.url,
            "nickname"    : new_user.nickname,
            "is_participant"    : new_user.is_participant,

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
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        member_id = data.get('member_id', None)
        password = data.get('password', None)

        user = authenticate(request, username=member_id , password = password)

        if user is not None:
            login(request, user)
            user_data = {
                "id"   : user.id,
                "password" : user.password,
                "member_id" : user.member_id,
                "name"    : user.name,
                "birth": user.birth,
                "bio":user.bio,
                #"avatar":user.avatar.url,
                "nickname":user.nickname,
                "is_participant":user.is_participant,
            }
            return JsonResponse({"success": True, "message" : "로그인 성공", "data" : user_data}, status = 200)
        else: 
            return JsonResponse({"success": False, "message": "로그인 실패"}, status = 403)

def logout_view(request): 
    logout(request)
    return JsonResponse({"success": True, "message": "로그아웃 성공"}, status = 200)





@require_http_methods(['GET','DELETE','POST'])
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
        
        

# Create your views here.
