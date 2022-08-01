import json
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from firebase_admin import messaging
from django.http.response import HttpResponseBadRequest, HttpResponse, HttpResponseServerError
from .models import Message
from django.core.serializers import serialize

User = get_user_model()


def message_save(user_id, message_data) -> None:
    user = get_object_or_404(User, id=user_id)

    new_message = Message.objects.create(
        user_id= user_id,
        content= message_data["content"]
    )

    new_message.save()


@require_http_methods("GET")
def read_messages_all(request, user_id):
    user = get_object_or_404(User,id=user_id)

    json_response_all = []
    messages = Message.objects.order_by("-id").filter(user_id=user_id)

    for message in messages:
        message_json = serialize(message)
        json_response_all.append(message_json)

    json_res = json.dumps(
        {
            "status": 200,
            "success": True,
            "message": "생성 성공!",
            "data": json_response_all
        },
        ensure_ascii=False
    )

    return HttpResponse(
        json_res,
        content_type=u"application/json; charset=utf-8mb4",
        status=200
    )


@require_http_methods("PATCH")
def register_token(request, user_id):
    body = json.loads(request.body.decode('utf8'))
    user = get_object_or_404(User, id=user_id)
    user.fcm_token = body["client_fcm_token"]
    user.save()

    return HttpResponse(status=200)


@require_http_methods("POST")
def send_message(request, family_id, user_id):
    body = json.loads(request.body.decode('utf8mb4'))
    registration_token = body["client_token"]
    receiver = get_object_or_404(User, id=user_id)

    if receiver.family_id == family_id:
        if registration_token == receiver.fcm_token:
            title = body.title
            content = body.content

            data = {
                "title": title,
                "content": content
            }

            message = messaging.Message(
                data=data,
                token=registration_token
            )

            try:
                response = messaging.send(message)
                print("메세지 전송 성공", response)
                message_save(receiver, data)
                return HttpResponse(status=200)
            except Exception as e:
                print("예외 발생", e)
                return HttpResponseServerError()

        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()




