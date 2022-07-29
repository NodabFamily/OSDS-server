from ast import BinOp
from django.shortcuts import render,get_object_or_404
from django.views.decorators.http import require_http_methods
import json
import bcrypt

from django.http import JsonResponse, HttpResponse
from accounts.models import User
from .models import Family

# Create your views here.
@require_http_methods(['POST', 'GET'])
def create_family(request):
    if request.method == "POST":
        image = request.FILES.get("cover_image")
        body = request.POST
        # sender = request.user
        
        password = body['password']
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),bcrypt.gensalt()
        )
        decoded_password = hashed_password.decode('utf_8')

        new_family = Family.objects.create(
            family_name = body['family_name'],
            cover_image = image,
            bio = body['bio'],
            password = decoded_password
        )

    
        # sender.is_participant = True
        # sender.family_id = new_family
        # sender.save()

        new_family_json = {
            "id" : new_family.id,
            "family_name" : new_family.family_name,
            "cover_image" : new_family.cover_image.url,
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


# @require_http_methods(['GET','POST'])
