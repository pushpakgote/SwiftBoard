from django.shortcuts import redirect
from django.urls import reverse_lazy,reverse
from django.shortcuts import get_object_or_404
from .models import Project
from teams.models import Team
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
from .forms import ProjectForm,AttachmentForm
from notifications.task import create_notification
from comments.models import Comment
from django.core.paginator import Paginator
from comments.forms import CommentForm
from django.contrib import messages

# Create your views here.
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_create.html'
    # success_url = reverse_lazy('accounts:dashboard')

    def get_initial(self):
        initial = super().get_initial()
        team_id = self.kwargs.get('team_id')
        if team_id:
            team = get_object_or_404(Team, pk=team_id)
            initial['team'] = team
        return initial

    def get_context_data(self, **kwargs):
        #latest notifications
        context=super().get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
            
        latest_notifications=self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()
        context["header_text"] = "Add Project"
        context["title"] = "Add Project"
        return context

    def form_valid(self, form):
        # form.instance.owner = self.request.user
        # return super().form_valid(form)
        project=form.save(commit=False)
        project.owner=self.request.user
        project.save()

        #send notification
        actor_username = self.request.user.username
        verb = f'New Project Assignment,{project.name}'
        object_id = project.id

        create_notification.delay(actor_username=actor_username, verb=verb, object_id=object_id)
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        team_id = self.kwargs.get('team_id')
        if team_id:
            # Redirect to the team detail page
            return reverse('teams:detail', args=[team_id])
        # Default fallback
        return reverse('accounts:dashboard')

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_create.html'
    success_url = reverse_lazy('accounts:dashboard')

    def get_context_data(self, **kwargs):
        #latest notifications
        context=super().get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
            
        latest_notifications=self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()
        context["header_text"] = "Update Project"
        context["title"] = "Update Project"
        return context

    def form_valid(self, form):
        # form.instance.owner = self.request.user
        # return super().form_valid(form)
        project=form.save(commit=False)
        project.owner=self.request.user
        project.save()

        #send notification
        actor_username = self.request.user.username
        verb = f'Updated Project: {project.name}'
        object_id = project.id

        create_notification.delay(actor_username=actor_username, verb=verb, object_id=object_id)
        return redirect(self.success_url)
    
class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        #latest notifications
        context=super().get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
            
        latest_notifications=self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()
        context["header_text"] = "Projects"
        context["title"] = "All Projects"
        return context
    
class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'teams/team_confirm_delete.html'
    success_url = reverse_lazy('projects:list')

    def get_context_data(self, **kwargs):
        #latest notifications
        context=super().get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
            
        latest_notifications=self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()
        context["header_text"] = "Projects"
        context["title"] = "All Projects"
        return context

class ProjectNearDueDateListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 5

    def get_queryset(self):
        return Project.objects.due_in_two_days_or_less()

    def get_context_data(self, **kwargs):
        #latest notifications
        context=super().get_context_data(**kwargs)
        latest_notifications=self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()
        context["header_text"] = "Due Projects"
        return context
    
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        #latest notifications
        context=super().get_context_data(**kwargs)
            
        latest_notifications=self.request.user.notifications.unread(self.request.user)
        project=self.get_object()
        comments=Comment.objects.filter_by_instance(project)
        paginator=Paginator(comments,10)
        page_number=self.request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()
        context["header_text"] = "Project Details"
        context["title"] = project.name
        context["my_company"] = "SwiftBoard"
        context["my_company_description"] = """This is SwiftBoard. Project tracking app"""
        context['page_obj'] = page_obj
        context['comment_count'] = comments.count()
        context['comment_form'] = CommentForm()
        context['attachment_form'] = AttachmentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        project=self.get_object()
        if request.user not in project.team.members.all():
            messages.warning(request, "You are not a member of this project. You don't have permission to comment")
            return self.get(request, *args, **kwargs)

        if 'comment_submit' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.content_object = project
                comment.save()

                #send notification
                actor_username = self.request.user.username
                actor_full_name = self.request.user.profile.full_name()
                verb = f'{actor_full_name} commented on {project.name}'
                print("Calling notification from project","Actor: ",actor_username," Verb: ",verb," Object Id: ",project.id)

                create_notification.delay(actor_username=actor_username, verb=verb, object_id=project.id)

                messages.success(request, 'Comment added successfully')
                return redirect('projects:project-detail', pk=project.pk)
            else:
                messages.warning(request, form.errors.get("comment",["An unknown error occured"][0]))
                # return redirect('projects:project-detail', pk=project.pk)
        
        if 'attachment_submit' in request.POST:
            print("Attachment submited")
            attachment_form = AttachmentForm(request.POST, request.FILES)
            if attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.user = request.user
                attachment.project = project
                attachment.save()
                messages.success(request, 'Attachment added successfully')
                return redirect('projects:project-detail', pk=project.pk)
            else:
                # messages.error(request, attachment_form.errors.get("file",["An unknown error occured"][0]))
                messages.error(request, "Error uploading attachment, plase try again")
                # return redirect('projects:project-detail', pk=project.pk)

        return self.get(request, *args, **kwargs)
    

class KanbanBoardView(DetailView):
    model = Project
    template_name = 'projects/kanbanboard.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        #latest notifications
        context=super().get_context_data(**kwargs)
            
        latest_notifications=self.request.user.notifications.unread(self.request.user)
        project=self.get_object()
        
        context['latest_notifications'] = latest_notifications[:3]
        context['notifications_count'] = latest_notifications.count()
        context["header_text"] = "Kanban Board"
        context["title"] = f"{project.name}'s Kanban Board"
        context['is_kanban'] = True

        #Seperate tasks by status
        context['backlog_tasks'] = project.tasks.filter(status='Backlog').upcomming()
        context['todo_tasks'] = project.tasks.filter(status='To Do').upcomming()
        context['in_progress_tasks'] = project.tasks.filter(status='In Progress').upcomming()
        context['completed_tasks'] = project.tasks.filter(status='Completed').upcomming()


        return context
    