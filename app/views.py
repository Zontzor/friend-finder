from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator

from django.forms import ValidationError
from django.views.generic.edit import UpdateView

from . import forms
from friendship.models import Friend, FriendshipRequest
from . models import User

from django.http import HttpResponseRedirect


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('app:login'))


class Landing(UpdateView):
    fields = "__all__"
    template_name = "app/landing.html"

    def get_context_data(self, **kwargs):
        context = super(Landing, self).get_context_data(**kwargs)

        try:
            friends = Friend.objects.friends(self.request.user)
        except:
            friends = {}

        context['friends'] = friends
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Landing, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return get_user_model().objects.get(pk=self.request.user.pk)


def login_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...friend_list
            # redirect to a new URL:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('app:landing'))
                else:
                    form.add_error(None, ValidationError(
                        "Your account is not active."
                    ))
            else:
                form.add_error(None, ValidationError(
                    "Invalid User Id of Password"
                ))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.LoginForm()

    return render(request, 'app/login.html', {'form': form})


def signup_view(request):
    if request.POST:
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = get_user_model().objects.get(username=username)
                if user:
                    form.add_error(None, ValidationError("This user already exists."))
            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create_user(username=username)

                # Set user fields provided
                user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()

                return redirect(reverse('app:login'))
    else:
        form = forms.SignupForm()

    return render(request, 'app/signup.html', {'form': form})


class UserProfile(UpdateView):
    form_class = forms.UserProfileForm
    template_name = "app/user_profile.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserProfile, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return get_user_model().objects.get(pk=self.request.user.pk)


def add_friend_view(request):
    if request.GET:
        form = forms.AddFriendForm()

    elif request.POST:
        form = forms.AddFriendForm(request.POST)
        if form.is_valid():
            try:
                other_user = User.objects.get(username=form.cleaned_data['username'])

                Friend.objects.add_friend(
                    request.user,  # The sender
                    other_user,  # The recipient
                    message='Hi! I would like to add you')  # This message is optional
            except:
                return redirect(reverse('app:friends'))

    else:
        form = forms.AddFriendForm()

    requests_sent = Friend.objects.sent_requests(user=request.user)
    requests_received = Friend.objects.unrejected_requests(user=request.user)

    return render(request, 'app/friends.html', {'form': form, 'requests_sent': requests_sent, 'requests_received': requests_received})


def manage_friend_request(request, operation, pk):
    friend_request = FriendshipRequest.objects.get(pk=pk)
    if operation == 'accept':
        friend_request.accept()
    elif operation == 'reject':
        friend_request.reject()
    return redirect('app:friends')

