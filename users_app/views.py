from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from .forms import UpdateProfileUser, UpdateUser, UserRegistryForm
from .models import User


class Registration(View):
    """
    Registration View, extended default User and RegistrationForm
    Profile of user created in signals.py
    """

    def get(self, request):
        form = UserRegistryForm()
        return render(request, "users_app/register.html", context={"form": form})

    def post(self, request):
        form = UserRegistryForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request,
                f"{username} Your Account has been created, You are now able to login",
            )
            return redirect("login")
        else:
            form = UserRegistryForm(request.POST)
        return render(request, "users_app/register.html", context={"form": form})


class ProfileUserUpdate(LoginRequiredMixin, View):
    """
    Update of user profile
    """

    def get(self, request):
        user_update_form = UpdateUser(instance=request.user)
        profile_user_update_form = UpdateProfileUser(instance=request.user.profileuser)

        return render(
            request,
            "users_app/profile.html",
            context={
                "user_update_form": user_update_form,
                "profile_user_update_form": profile_user_update_form,
            },
        )

    def post(self, request):
        user_update_form = UpdateUser(request.POST, instance=request.user)
        profile_user_update_form = UpdateProfileUser(
            request.POST, request.FILES, instance=request.user.profileuser
        )
        if user_update_form.is_valid() and profile_user_update_form.is_valid():
            user_update_form.save()
            profile_user_update_form.save()
            messages.success(request, "Edited", fail_silently=True)
            return redirect("profile")
        else:
            user_update_form = UpdateUser(instance=request.user)
            profile_user_update_form = UpdateProfileUser(
                instance=request.user.profileuser
            )
            messages.error(request, "Wrong Data", fail_silently=True)

        return render(
            request,
            "users_app/profile.html",
            context={
                "user_update_form": user_update_form,
                "profile_user_update_form": profile_user_update_form,
            },
        )


class DeleteUser(LoginRequiredMixin, DeleteView):
    """
    delete of user
    USER can be deleted only by him self
    """

    model = User
    success_url = reverse_lazy("homepage")
    template_name = "users_app/user_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.request.user.id == self.get_object().id:
            self.object.delete()
        else:
            messages.error(request, "Access Denied")
            return redirect("profile")
        messages.success(request, "deleted")
        return HttpResponseRedirect(success_url)
