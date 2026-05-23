from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from team_finder.utils import get_paginator

from .constants import *
from .forms import ProjectForm
from .models import Project


def index(request):
    query_set = Project.objects.all().order_by("-id")
    paginator = get_paginator(request, query_set)
    context = {"page_obj": paginator}
    return render(request, "projects/project_list.html", context)


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related("owner")
        .prefetch_related("participants")
        .annotate(participants_count=Count("participants")),
        id=project_id,
    )
    context = {"project": project}
    return render(request, "projects/project-details.html", context)


@login_required
def toggle_completion(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if (
        project.owner == request.user
        and request.method == "POST"
        and project.status == STATUS_OPEN
    ):
        project.status = STATUS_CLOSED
        project.save()
        return JsonResponse(
            {"status": "ok", "project_status": "closed"}
        )
    return JsonResponse(
        {"status": "Wrong method or project already closed"},
        status=HTTPStatus.BAD_REQUEST,
    )


@login_required
def toggle_participation(request, project_id):
    if request.method != "POST":
        return JsonResponse(
            {"status": "Wrong method"}, status=HTTPStatus.BAD_REQUEST
        )
    project = get_object_or_404(Project, id=project_id)
    user = request.user
    if user in project.participants:
        project.participants.remove(user)
    else:
        project.participants.add(user)
    return JsonResponse({"status": "ok"})


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            project = form.save(commit=False)
            user = request.user
            project.owner = user
            project.save()
            project.participants.add(user)
            return redirect(
                "projects:project_detail", project_id=project.id
            )

    context = {"form": form, "is_edit": False}

    return render(request, "projects/create-project.html", context)


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user != project.owner:
        return redirect(
            "projects:project_detail", project_id=project_id
        )
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(
                "projects:project_detail", project_id=project_id
            )
    context = {"form": form, "is_edit": True}
    return render(request, "projects/create-project.html", context)
