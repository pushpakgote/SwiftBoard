from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Team
from .forms import TeamForm


# Create your views here.
    
class TeamListView(ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        latest_notifications=self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()
        context["header_text"] = "Teams"
        context["title"] = "All Teams"
        return context

class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'
    success_url = reverse_lazy('teams:list')

    def form_valid(self, form):
        team=form.save(commit=False)
        team.created_by=self.request.user
        team.save()
        form.save_m2m()
        return redirect(self.success_url)


    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        latest_notifications=self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()
        context["header_text"] = "Teams"
        context["title"] = "All Teams"
        return context

    
class TeamDetailView(DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        latest_notifications=self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()
        context["header_text"] = "Team Details"
        context["title"] = "Team Details"
        return context
    
class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'
    success_url = reverse_lazy('teams:list')

    def form_valid(self, form):
        team=form.save(commit=False)
        team.created_by=self.request.user
        team.save()
        form.save_m2m()
        return redirect(self.success_url)


    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        latest_notifications=self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()
        context["header_text"] = "Update Team"
        context["title"] = "Update Team"
        return context
    
class TeamDeleteView(DeleteView):
    model = Team
    template_name = 'teams/team_confirm_delete.html'
    success_url = reverse_lazy('teams:list')

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        latest_notifications=self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()
        context["header_text"] = "Delete Team"
        context["title"] = "Delete Team"
        return context
    