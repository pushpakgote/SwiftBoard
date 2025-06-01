from django.urls import path
from .views import ProjectCreateView,ProjectListView,ProjectNearDueDateListView,ProjectDetailView,ProjectUpdateView,KanbanBoardView,ProjectDeleteView


app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name='list'),
    path('near-due-date/', ProjectNearDueDateListView.as_view(), name='due-list'),
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('create/team/<int:team_id>/', ProjectCreateView.as_view(), name='create-for-team'),
    path('<uuid:pk>/update/', ProjectUpdateView.as_view(), name='update'),
    path('<uuid:pk>', ProjectDetailView.as_view(), name='project-detail'),
    path('<uuid:pk>/kanban-board/', KanbanBoardView.as_view(), name='kanban-board'),
    path('<uuid:pk>/delete/', ProjectDeleteView.as_view(), name='delete'),
]