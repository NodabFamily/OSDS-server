import json
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from firebase_admin import messaging
from django.http.response import HttpResponseBadRequest, HttpResponse, HttpResponseServerError

User = get_user_model()


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

            message = messaging.Message(
                data={
                    "title": title,
                    "content": content,
                },
                token=registration_token
            )

            try:
                response = messaging.send(message)
                print("메세지 전송 성공", response)
                return HttpResponse(status=200)
            except Exception as e:
                print("예외 발생", e)
                return HttpResponseServerError()

        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()






