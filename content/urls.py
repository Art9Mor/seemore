from django.urls import path

from content.apps import ContentConfig
from content import views

app_name = ContentConfig.name

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', views.contacts, name='contacts_info'),

    # Content URLs
    path('content/', views.ContentListView.as_view(), name='content_list'),
    path('content_paid_list/', views.ContentPaidListView.as_view(), name='content_paid_list'),
    path('content_free_list/', views.ContentFreeListView.as_view(), name='content_free_list'),
    path('content/<int:pk>/', views.ContentDetailView.as_view(), name='content_detail'),
    path('content/create/', views.ContentCreateView.as_view(), name='content_create'),
    path('content/<int:pk>/update/', views.ContentUpdateView.as_view(), name='content_update'),
    path('content/<int:pk>/delete/', views.ContentDeleteView.as_view(), name='content_delete'),
    path('content_success_create/', views.content_success_create, name='content_success_create'),

    # Author URLs
    path('author_list/', views.AuthorListView.as_view(), name='author_list'),
    path('become_author/', views.BecomeAuthorView.as_view(), name='become_author'),
    path('author/<int:pk>/detail/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('an_author/', views.an_author, name='an_author'),
    path('author/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author_delete'),
    path('<int:pk>/author_content/', views.author_content, name='author_content'),

    # Report URLs
    path('content/<int:pk>/reports/', views.ReportListView.as_view(), name='report_list'),
    path('report/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('report/create/<int:pk>/', views.ReportCreateView.as_view(), name='report_create'),
    path('report/delete/<int:pk>/', views.ReportDeleteView.as_view(), name='report_delete'),
    path('report_success_create/', views.report_success_create, name='report_success_create'),
]
