from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import ReferendumForm
from .models import *
from django.contrib.auth.decorators import login_required
from referendaMain.decorators import (
    unauthenticated_user,
    admin_only,
    prevent_duplicate_vote,
    voter_only,
    unavailable_referendum,
)
from .forms import CreateUserForm, CustomPasswordResetForm, SetPasswordForm
from braces.views import CsrfExemptMixin, SetHeadlineMixin
from django.core.cache import cache
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db.models.query_utils import Q

# Create your views here.


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request,
            "Thank you for confirming your email, your account is now activated and you can now access the website.",
        )
        return redirect("login")
    else:
        messages.error(request, "The activation link is invalid!")
    return redirect("login")


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string(
        "referendaPages/activate_account.html",
        {
            "user": user.username,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )

    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(
            request,
            f"Account successfully created for {str(user)}, please activate your account by clicking the activation link in your confirmation e-mail.",
        )
    else:
        message.error(
            request,
            f"there is a problem sending email to {to_email}, check if it is typed correctly",
        )


# Registering
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            activateEmail(request, user, form.cleaned_data.get("email"))
            return redirect("login")

    context = {"form": form}
    return render(request, "referendaPages/register.html", context)


@unauthenticated_user
def resetPassword(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            user_username = form.cleaned_data["username"]
            user_email = form.cleaned_data["email"]
            associated_user = (
                get_user_model()
                .objects.filter(Q(username=user_username, email=user_email))
                .first()
            )
            if associated_user:
                subject = "Password Reset Request"
                message = render_to_string(
                    "referendaPages/password_reset_template.html",
                    {
                        "user": associated_user,
                        "domain": get_current_site(request).domain,
                        "uid": urlsafe_base64_encode(force_bytes(associated_user.pk)),
                        "token": account_activation_token.make_token(associated_user),
                        "protocol": "https" if request.is_secure() else "http",
                    },
                )

            email = EmailMessage(subject, message, to=[associated_user.email])
            if email.send():
                messages.success(
                    request,
                    """
                An email for a password reset has been sent to your email account.
                """,
                )
            else:
                message.error(
                    request,
                    f"there is a problem sending a password reset email to {associated_user}, check if it is typed correctly",
                )
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
        return redirect("password_reset")

    form = CustomPasswordResetForm()
    return render(
        request=request,
        template_name="referendaPages/password_reset.html",
        context={"form": form},
    )


@unauthenticated_user
def resetPasswordConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set!")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        form = SetPasswordForm(user)
        return render(request, "referendaPages/set_password.html")
    else:
        messages.error(request, "The link is invalid!")
    messages.error(request, "Something went wrong, going back to login")
    return redirect("login")


class loginPage(CsrfExemptMixin, SetHeadlineMixin, LoginView):
    template_name = "referendaPages/login.html"
    form_class = AuthenticationForm
    headline = "Login"

    @method_decorator(unauthenticated_user)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(request=self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return redirect("dashboard")

    def form_invalid(self, form):
        username = form.cleaned_data.get("username", "")
        self.increment_login_attempts()

        user = User.objects.filter(username=username).first()

        if user and not user.is_active:
            messages.error(
                self.request,
                "Your account is not active. Please activate your account.",
            )
        else:
            messages.error(self.request, "Username or password is incorrect.")

        return super().form_invalid(form)

    def increment_login_attempts(self):
        username = self.request.POST.get("username", "")
        attempts = cache.get("login_attempts_{}".format(username), 0)
        attempts += 1
        cache.set("login_attempts_{}".format(username), attempts, timeout=60)

        if attempts >= 5:
            messages.error(
                self.request, "Too many unsuccessful login attempts. Try again later."
            )


def logoutUser(request):
    logout(request)
    return redirect("login")


# Dashboard
@login_required(login_url="login")
def dashboard(request):
    current_date = datetime.now().date()
    referendums = Referendum.objects.all()

    return render(
        request,
        "referendaPages/dashboard.html",
        context={"referendums": referendums, "current_date": current_date},
    )


# Editing account information
@voter_only
@login_required(login_url="login")
def accountUpdate(request):
    voter = Voter.objects.get(user=request.user)
    if request.method == "POST":
        new_first_name = request.POST.get("first_name")
        new_last_name = request.POST.get("last_name")
        new_email = request.POST.get("email")
        voter.first_name = new_first_name
        voter.last_name = new_last_name
        voter.email = new_email
        voter.phone = request.POST.get("phone")
        voter.save()

        user = voter.user
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.email = new_email
        user.save()
        messages.success(request, "Account Updated successfully!")
        return redirect("account")

    context = {"voter": voter}
    return render(request, "referendaPages/account.html", context)


# Create Referendum
@login_required(login_url="login")
@admin_only
def createReferendumPage(request):
    all_choices = Choice.objects.all()
    if request.method == "POST":
        form = ReferendumForm(request.POST)
        if form.is_valid():
            referendum = form.save(commit=False)
            choices_data = request.POST.getlist("choices")

            # Server-side validation: Check if at least two options are selected
            if len(choices_data) < 2:
                messages.error(request, "Please select at least two options.")
                return redirect("create")

            referendum.save()
            referendum.choices.set(choices_data)
            referendum.save()

            messages.success(request, "Referendum created successfully!")
            return redirect("create")
        else:
            messages.error(request, "Referendum created failed!")
            return redirect("create")
    else:
        form = ReferendumForm()

    context = {"form": form, "all_choices": all_choices}
    return render(request, "referendaPages/create.html", context)


# Voting
@voter_only
@prevent_duplicate_vote
@unavailable_referendum
def votePage(request, id):
    referendum = Referendum.objects.get(id=id)

    if request.method == "POST":
        referendum_id = request.POST.get("referendum_id")
        voter_id = request.POST.get("voter_id")
        choice_id = request.POST.get("choice_id")
        try:
            referendum = Referendum.objects.get(id=referendum_id)
            voter = Voter.objects.get(id=voter_id)
            choice = Choice.objects.get(id=choice_id)

            if Vote.objects.create(voter=voter, referendum=referendum, choice=choice):
                messages.success(request, "Vote submitted successfully!")
                return redirect("dashboard")

        except (Referendum.DoesNotExist, Voter.DoesNotExist, Choice.DoesNotExist):
            messages.error(
                request, "Please select a choice before submitting your vote!"
            )

    return render(
        request, "referendaPages/vote.html", context={"referendum": referendum}
    )


# Results
@login_required(login_url="login")
def resultsPage(request, id):
    referendum = Referendum.objects.get(id=id)
    total_voters = Voter.objects.count()
    total_votes = Vote.objects.filter(referendum=referendum).count()
    unvoted = total_voters - total_votes
    yes_votes = Vote.objects.filter(referendum=referendum, choice_id=1).count()
    no_votes = Vote.objects.filter(referendum=referendum, choice_id=2).count()
    vote_results = []
    for choice in referendum.choices.all():
        voteCount = Vote.objects.filter(referendum=referendum, choice=choice).count()
        vote_results.append([choice.name, voteCount])

    return render(
        request,
        "referendaPages/results.html",
        context={
            "referendum": referendum,
            "unvoted": unvoted,
            "yes_votes": yes_votes,
            "no_votes": no_votes,
            "vote_results": vote_results,
            "total_votes": total_votes,
        },
    )
