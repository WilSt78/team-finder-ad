from django.contrib.auth import (
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from team_finder.utils import get_paginator

from .forms import (
    ChangePasswordForm,
    EditForm,
    LoginForm,
    RegistrationForm,
)
from .models import Skill, User


def get_users(request):
    active_skill = request.GET.get("skill")
    if active_skill:
        query_set = (
            User.objects.prefetch_related("skills")
            .filter(skills__name=active_skill)
            .order_by("id")
        )
    else:
        query_set = (
            User.objects.prefetch_related("skills")
            .all()
            .order_by("id")
        )
    paginator = get_paginator(request, query_set)
    all_skills = Skill.objects.all()
    context = {
        "page_obj": paginator,
        "all_skills": all_skills,
        "active_skill": active_skill,
    }
    return render(request, "users/participants.html", context)


def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {"user": user}
    return render(request, "users/user-details.html", context)


def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("/projects/list/")
    context = {"form": form}
    return render(request, "users/register.html", context)


def login_view(request):
    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("projects:project_list")
    context = {"form": form}
    return render(request, "users/login.html", context)


@login_required
def edit_profile(request):
    form = EditForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    if form.is_valid():
        form.save()
        return redirect("users:user_details", user_id=request.user.id)
    context = {"form": form}
    return render(request, "users/edit_profile.html", context)


@login_required
def change_password(request):
    form = ChangePasswordForm(request.POST or None)
    user = request.user
    if form.is_valid():
        if user.check_password(form.cleaned_data["old_password"]):
            user.set_password(form.cleaned_data["new_password1"])
            user.save()
            update_session_auth_hash(request, user)
            return redirect("users:user_details", user_id=user.id)
    context = {"form": form}
    return render(request, "users/change_password.html", context)


@login_required
def logout_view(request):
    logout(request)
    return redirect("projects:project_list")
