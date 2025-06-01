from django.urls import path
from .views import DashboardView,MemberListView,RegisterView, ProfileUpdateView, ProfileDetailView

app_name = 'accounts'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('members/', MemberListView.as_view(), name='members-list'),
    path('register/', RegisterView, name='register'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
]
