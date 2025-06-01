from django.shortcuts import render,redirect
from django.views.generic import View,ListView,DetailView
from django.contrib.auth.decorators import login_not_required
from projects.models import Project
from tasks.models import Task
from .models import Profile
from teams.models import Team # Assuming Team model might be needed for context, otherwise removable
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404


# Create your views here.
@login_not_required
def RegisterView(request):
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
        else:
            messages.error(request, 'Account not created')
    else:
        form=RegisterForm()

    return render(request, 'registration/register.html',{'form':form})

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        # latest_projects = Project.objects.order_by('-created_at')[:5]
        latest_projects = Project.objects.all()
        latest_tasks=Task.objects.all()
        latest_members=Profile.objects.all()
        context = {}
        # if request.user.is_authenticated:
        latest_notifications=request.user.notifications.unread(request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()

        context['latest_projects'] = latest_projects[:5]
        context['latest_project_count'] = latest_projects.count()
        context['projects_near_due_date'] = latest_projects.due_in_two_days_or_less()[:5]
        context['latest_task_count'] = latest_tasks.count()
        context['latest_members'] = latest_members[:8]
        context['latest_member_count'] = latest_members.count()
        context["team_count"] = Team.objects.count()
        context["header_text"] = "Dashboard"
        context["title"] = "Dashboard"
        return render(request, 'accounts/dashboard.html', context)
    

class MemberListView(ListView):
    model = Profile
    template_name = 'accounts/profile_list.html'
    context_object_name = 'members'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        #latest notifications
        context=super().get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
            
        latest_notifications=self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()
        context["header_text"] = "Projects"
        context["title"] = "All Members"
        return context

class ProfileDetailView(View):
    template_name = 'accounts/profile_detail.html'

    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=pk)
        user = profile.user

        context = {
            'user_profile': user, # Pass the whole user object
            'profile_data': profile, # Pass the profile object
            'title': 'Profile',
            'header_text': f"Profile"
        }

        latest_notifications = request.user.notifications.unread(request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()

        return render(request, self.template_name, context)

class ProfileUpdateView(View):
    template_name = 'accounts/profile_edit.html'

    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile,user=request.user)
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'title': 'Edit Profile',
            'header_text': 'Edit Profile'
        }
        
        latest_notifications = request.user.notifications.unread(request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()
        
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile,user=request.user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile-detail', pk=request.user.profile.pk ) # Redirect to detail view after saving
        else:
            messages.error(request, 'Please correct the errors below.')

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'title': 'Edit Profile',
            'header_text': 'Edit Profile'
        }

        latest_notifications = request.user.notifications.unread(request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()

        return render(request, self.template_name, context)
    