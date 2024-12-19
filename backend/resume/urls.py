from django.urls import path
from .views import ResumeUploadView, ResumeRewriteView, ResumeListView, download_resume, JobMatchingView
from . import views

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='upload_resume'),
    path('rewrite/<int:pk>/', ResumeRewriteView.as_view(), name='rewrite_resume'),
    path('api/resumes/', ResumeListView.as_view(), name='resume_list'),
    # path('search_jobs/', JobSearchView.as_view(), name='search_jobs'),
    path('download/<str:file_name>/', views.download_resume, name='download'),
    path('match-jobs/', JobMatchingView, name='match-jobs'),
]
