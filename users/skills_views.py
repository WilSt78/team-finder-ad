import json
from http import HTTPStatus

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Skill, User

@login_required
def add_skill(request, user_id):
    if request.user.id != user_id:
        return JsonResponse({
            "status" : "error",
            "message" : "Навыки можно добавлять только на свой профиль"},
            status=HTTPStatus.FORBIDDEN
        )
    data = json.loads(request.body)
    name = data.get('name')
    skill_id = data.get('skill_id')
    user = get_object_or_404(User, id=user_id)

    if name:
        skill, created = Skill.objects.get_or_create(name=name)
    if skill_id:
        skill = get_object_or_404(Skill, id=skill_id)
    
    if not user.skills.filter(id=skill.id).exists():
        user.skills.add(skill)
        return JsonResponse({
            'id': skill.id,
            'name': skill.name,
            'created': created,
            'added': True
        })
    
    return JsonResponse({
        "status" : "error",
        "message" : "У этого пользователя уже есть такой навык"},
        status = HTTPStatus.BAD_REQUEST)

@login_required
def remove_skill(request, user_id, skill_id):
    if request.method != 'POST':
        return JsonResponse(
            {"status" : "Wrong method"},
            status = HTTPStatus.BAD_REQUEST
        )
    user = get_object_or_404(User, id= user_id)
    if user!=request.user:
        return JsonResponse({
            "status" : "error",
            "message" : "Вы можете удалять только свои навыки"},
            status=HTTPStatus.FORBIDDEN)
    skill = get_object_or_404(Skill, id = skill_id)
    user.skills.remove(skill)
    return JsonResponse({"status" : "ok"})
