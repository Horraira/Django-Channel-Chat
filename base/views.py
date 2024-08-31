from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
import random
import time
import json
from .models import RoomMember
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def get_token(request):
    app_id = 'd24670d9480a443ebd774621d086a64a'
    app_certificate = '5032b09581ec46179b30e6721e3c0fdd'
    channel_name = request.GET.get('channel')
    uid = random.randint(1, 230)
    expiration_time_in_seconds = 3600 * 24
    current_timestamp = time.time()
    privilege_expired_ts = current_timestamp + expiration_time_in_seconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(app_id, app_certificate, channel_name, uid, role, privilege_expired_ts)
    return JsonResponse({'token':token,
                         'uid':uid}, safe=False)

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')

@csrf_exempt
def create_user(request):
    data = json.loads(request.body)

    RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['uid'],
        room_name=data['room_name']
    )
    return JsonResponse({'name':data['name']}, safe=False)

def get_members(request):
    uid = request.GET.get('uid')
    room_name = request.GET.get('room_name')
    try:
        member = RoomMember.objects.filter(room_name=room_name).exclude(uid=uid)
    except RoomMember.DoesNotExist:
        return JsonResponse('No members found', safe=False)
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def delete_member(request):
    data = json.loads(request.body)
    try:
        member = RoomMember.objects.get(
            room_name=data['room_name'], 
            uid=data['uid'],
            name=data['name']
            )
        member.delete()
    except RoomMember.DoesNotExist:
        return JsonResponse('Member does not exist', safe=False)
    return JsonResponse('Member was deleted', safe=False)