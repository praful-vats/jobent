from django.urls import path
from .views import ResumeUploadView, ResumeRewriteView, ResumeListView

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='upload_resume'),
    path('rewrite/<int:pk>/', ResumeRewriteView.as_view(), name='rewrite_resume'),
    path('api/resumes/', ResumeListView.as_view(), name='resume_list'),
    # path('search_jobs/', JobSearchView.as_view(), name='search_jobs'),
]
