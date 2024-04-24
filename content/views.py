from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from pytils.translit import slugify

from users.models import PaymentSubscription, User
from .forms import ContentForm
from .models import Content, Report, Author
from .paginators import ContentPaginator


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
    contact_info = {
        'email': 'seemoret@example.com',
        'phone': '+1234567890',
        'address': '123 Street, City, Country',
        'telegram': '@seemore',
    }
    return render(request, 'content/contacts.html', {'contact_info': contact_info})


class ContentListView(ListView):
    """
    List all contents based on access rights.
    """
    model = Content
    template_name = 'content/content_list.html'
    context_object_name = 'content_list'
    paginate_by = 9
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = ContentPaginator(self.object_list, self.paginate_by)
        page_number = self.request.GET.get('page')

        if page_number is None:
            page_number = 1

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context['page_obj'] = page_obj
        return context


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
        self.obj = super().get_object(queryset)
        self.obj.views_count += 1
        self.obj.save()
        if self.obj.paid_only and not self.request.user.is_subscribed:
            raise Http404("Content not found")
        return self.obj


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
        if form.is_valid():
            instance = form.save(commit=False)
            if self.request.user.is_author:
                instance.author = self.request.user
                instance.slug = slugify(instance.title)
                instance.save()
                author = self.request.user.author
                author.article_count += 1
                author.save()
                messages.success(self.request, 'Content created successfully!')
                return super().form_valid(form)
            else:
                messages.error(self.request, 'You are not authorized to create content.')
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)


class ContentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update an existing content.
    """
    model = Content
    form_class = ContentForm
    template_name = 'content/content_form.html'

    def test_func(self):
        content = self.get_object()
        return self.request.user == content.author

    def handle_no_permission(self):
        return render(self.request, 'content/content_no_permission.html')

    def get_success_url(self):
        return reverse('content:content_detail', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = self.request.user
            instance.slug = slugify(instance.title)
            instance.save()
        return super().form_valid(form)


class ContentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
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

    def test_func(self):
        """
        Determine if a user is allowed to delete content.
        """
        if super().has_permission():
            return self.request.user.is_superuser or self.request.user.groups.filter(name='Moderators').exists()
        return False


class ReportCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new report.
    """
    model = Report
    fields = ['content', 'comment']
    success_url = reverse_lazy('content:content_list')
    extra_context = {
        'title': 'Create Report',
    }

    def form_valid(self, form):
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = self.request.user
            instance.slug = slugify(instance.title)
            instance.save()
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
    permission_required = 'content.delete_report'

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
    context_object_name = 'reports'
    extra_context = {
        'title': 'Report List',
    }

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        content_id = self.kwargs.get('content_id')
        queryset = queryset.filter(content_id=content_id)
        return queryset


class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'content/report_detail.html'
    context_object_name = 'report_detail'
    extra_context = {
        'title': 'Report Detail',
    }

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.is_staff


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


class AuthorListView(ListView):
    model = Author
    template_name = 'content/author_list.html'
    context_object_name = 'author_list'
    extra_context = {
        'title': 'All authors',
    }


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'content/author_detail.html'
    context_object_name = 'author'
    extra_context = {
        'title': 'Author',
    }


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
