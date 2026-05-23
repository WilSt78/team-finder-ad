from django.http import JsonResponse

from .constants import SKILL_QUERY_SIZE
from .models import Skill


def search_skills(request):
    query = request.GET.get("q", "").strip()
    skills_queryset = Skill.objects.filter(
        Q(name__istartswith=query)
    ).order_by("name")[:SKILL_QUERY_SIZE]
    skills_data = [
        {"id": skill.id, "name": skill.name}
        for skill in skills_queryset
    ]
    return JsonResponse(skills_data, safe=False)
