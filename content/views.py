from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View, FormView

from users.models import PaymentSubscription, User
from .forms import ContentForm
from .models import Content, Report, Author


class HomeView(TemplateView):
    template_name = 'content/home.html'
    extra_context = {
        'title': 'Home Page',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Content.objects.all()[:3]
        return context_data


def contacts(request):
    context = {
        'title': 'SeeMore: contact info'
    }
    return render(request, 'content/contacts.html', context)


class ContentListView(ListView):
    """
    List all contents based on access rights.
    """
    model = Content
    template_name = 'content/content_list.html'
    context_object_name = 'content_list'
    extra_context = {
        'title': 'Content List',
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.filter(paid_only=False)
        else:
            user_subscribed = PaymentSubscription.objects.filter(user=self.request.user, is_active=True).exists()
            if user_subscribed:
                return queryset
            else:
                return queryset.filter(paid_only=False)


class ContentDetailView(DetailView):
    """
    Detail view of content.
    """
    model = Content
    template_name = 'content/content_detail.html'
    context_object_name = 'content'
    extra_context = {
        'title': 'Content Detail',
    }

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.paid_only and not self.request.user.is_subscribed:
            raise Http404("Content not found")
        return obj


class ContentCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new content.
    """
    model = Content
    form_class = ContentForm
    template_name = 'content/content_form.html'
    success_url = reverse_lazy('content:content_list')
    extra_context = {
        'title': 'Create Content',
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ContentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update an existing content.
    """
    model = Content
    form_class = ContentForm
    template_name = 'content/content_form.html'
    success_url = reverse_lazy('content:content_list')
    extra_context = {
        'title': 'Update Content',
    }

    def test_is_author(self):
        content = self.get_object()
        return self.request.user == content.author

    def handle_no_permission(self):
        return render(self.request, 'content/content_no_permission.html')


class ContentDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Delete an existing content.
    """
    model = Content
    success_url = reverse_lazy('content:content_list')
    template_name = 'content/content_confirm_delete.html'
    permission_required = 'content.delete_content'
    extra_context = {
        'title': 'Delete Content',
    }

    def has_permission(self):
        """
        Determine if a user is allowed to delete content.
        """
        if super().has_permission():
            # Проверяем, является ли текущий пользователь модератором или суперпользователем
            return self.request.user.is_superuser or self.request.user.groups.filter(name='Moderators').exists()
        return False


class ReportCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new report.
    """
    model = Report
    fields = ['content', 'comment']
    template_name = 'content/report_create.html'
    success_url = reverse_lazy('content:content_list')
    extra_context = {
        'title': 'Create Report',
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Moderators').exists():
            context['user'] = self.request.user
        return context


class ReportDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Delete an existing report.
    """
    model = Report
    success_url = reverse_lazy('content:content_list')
    template_name = 'content/report_delete.html'
    permission_required = 'content.delete_report'
    extra_context = {
        'title': 'Delete Report',
    }

    def has_permission(self):
        """
        Determine if a user is allowed to delete a report.
        """
        if super().has_permission():
            # Check if the user is a moderator or superuser
            return self.request.user.is_superuser or self.request.user.groups.filter(name='Moderators').exists()
        return False


class ReportListView(LoginRequiredMixin, ListView):
    """
    List all reports.
    """
    model = Report
    template_name = 'content/report_list.html'
    context_object_name = 'report_list'
    extra_context = {
        'title': 'Report List',
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Moderators').exists():
            return queryset
        return queryset.filter(user=user) | queryset.filter(content__author=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


# class AuthorAutocompleteView(FormView):
#     template_name = 'content/author_list.html'
#     form_class = AuthorAutocompleteForm
#
#     def form_valid(self, form):
#         return JsonResponse({'html': form.as_p(), 'url': reverse_lazy('author_info')})
#
#
# class ContentAutocompleteView(FormView):
#     template_name = 'content/author_list.html'
#     form_class = ContentAutocompleteForm
#
#     def form_valid(self, form):
#         authors = User.objects.filter(username__icontains=form.cleaned_data['author'])
#         author_list = [{'id': author.id, 'text': author.username} for author in authors]
#         return JsonResponse({'results': author_list})
#
#
# class AuthorInfoView(View):
#     def get(self, request, *args, **kwargs):
#         author_id = request.GET.get('author_id')
#         author = User.objects.get(pk=author_id)
#         author_contents = Content.objects.filter(author=author)
#         return JsonResponse({
#             'author': {
#                 'id': author.id,
#                 'username': author.username,
#                 'full_name': author.full_name,
#                 'avatar_url': author.avatar.url if author.avatar else None
#             },
#             'author_contents': [{'title': content.title, 'category': content.category} for content in author_contents]
#         })


class BecomeAuthorView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user

        if user.is_author:
            return JsonResponse({'message': 'You are already an author.'}, status=400)

        user.is_author = True
        user.save()

        author = Author.objects.create(user=user)

        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(content_type=content_type, codename='add_content')
        user.user_permissions.add(permission)

        return JsonResponse({'message': 'You have become an author!'})
