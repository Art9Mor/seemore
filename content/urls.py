from django.urls import path

from content.apps import ContentConfig
from content.views import ContentListView, ContentDetailView, ContentCreateView, ContentUpdateView, ContentDeleteView, \
    ReportListView, ReportCreateView, ReportDeleteView, HomeView, AuthorListView, BecomeAuthorView, contacts

app_name = ContentConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),

    # Content URLs
    path('content/', ContentListView.as_view(), name='content_list'),
    path('content/<int:pk>/', ContentDetailView.as_view(), name='content_detail'),
    path('content/create/', ContentCreateView.as_view(), name='content_create'),
    path('content/update/<int:pk>/', ContentUpdateView.as_view(), name='content_update'),
    path('content/delete/<int:pk>/', ContentDeleteView.as_view(), name='content_delete'),

    path('author_list/', AuthorListView.as_view(), name='author_list'),
    path('become_author/', BecomeAuthorView.as_view(), name='become_author'),

    # Report URLs
    path('report/', ReportListView.as_view(), name='report_list'),
    path('report/create/', ReportCreateView.as_view(), name='report_create'),
    path('report/delete/<int:pk>/', ReportDeleteView.as_view(), name='report_delete'),
]
