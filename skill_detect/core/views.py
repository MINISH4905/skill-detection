from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, DomainSelectionForm


# ===============================
# HOME REDIRECT
# ===============================
def home_redirect(request):
    """
    Redirect user based on authentication status.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


# ===============================
# REGISTER
# ===============================
def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.role = form.cleaned_data.get('role')
            user.save()

            login(request, user)
            return redirect('dashboard')

    return render(request, "core/register.html", {"form": form})


# ===============================
# LOGIN
# ===============================
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')

    return render(request, "core/login.html", {"form": form})


# ===============================
# DASHBOARD
# ===============================

@login_required
def dashboard(request):
    user = request.user

    if user.selected_domains.count() == 0:
        return redirect("select_domains")

    domains = user.selected_domains.all()

    return render(request, "dashboard.html", {
        "domains": domains,
        "domain_count": domains.count()
    })


@login_required
def select_domains(request):
    user = request.user   # ✅ use custom User directly

    if request.method == "POST":
        form = DomainSelectionForm(request.POST)

        if form.is_valid():
            user.selected_domains.set(form.cleaned_data['domains'])
            return redirect("dashboard")
    else:
        form = DomainSelectionForm(
            initial={'domains': user.selected_domains.all()}
        )

    return render(request, "select_domains.html", {"form": form})


# ===============================
# LOGOUT
# ===============================
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def select_domains(request):
    profile = request.user

    if request.method == "POST":
        form = DomainSelectionForm(request.POST)
        if form.is_valid():
            profile.selected_domains.set(form.cleaned_data['domains'])
            return redirect("dashboard")
    else:
        form = DomainSelectionForm(
            initial={'domains': profile.selected_domains.all()}
        )

    return render(request, "select_domains.html", {"form": form})

