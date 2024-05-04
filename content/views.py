from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from pytils.translit import slugify

from .forms import ContentForm, ReportForm
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
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.request.user
        if self.object.paid_only and not (
                user.is_superuser or user.is_staff or user.is_subscribed or user == self.object.author.user
        ):
            return redirect(reverse('users:must_subscribe'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Content Detail'
        return context


class ContentCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new content.
    """
    model = Content
    form_class = ContentForm
    template_name = 'content/content_form.html'
    success_url = reverse_lazy('content:content_success_create')
    extra_context = {
        'title': 'Create Content',
    }

    def form_valid(self, form):
        if form.is_valid():
            instance = form.save(commit=False)
            if self.request.user.is_author:
                author = self.request.user.author
                instance.author = author
                instance.slug = slugify(instance.title)
                instance.save()

                author.article_count += 1
                author.save()
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
        user = self.request.user
        return user == content.author.user or user.is_superuser or user.is_staff

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


class ContentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete an existing content.
    """
    model = Content
    success_url = reverse_lazy('content:content_list')
    extra_context = {
        'title': 'Delete Content',
    }

    def test_func(self):
        content = self.get_object()
        user = self.request.user
        return user == content.author.user or user.is_superuser or user.is_staff


class ContentPaidListView(LoginRequiredMixin, ListView):
    """
    List all paid content.
    """
    model = Content
    template_name = 'content/content_paid_list.html'
    context_object_name = 'content_paid_list'
    paginate_by = 9

    def get_queryset(self):
        return Content.objects.filter(paid_only=True)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('users:must_register'))
        return super().dispatch(request, *args, **kwargs)


class ContentFreeListView(ListView):
    """
    List all free content.
    """
    model = Content
    template_name = 'content/content_free_list.html'
    context_object_name = 'content_free_list'
    paginate_by = 9

    def get_queryset(self):
        return Content.objects.filter(paid_only=False)


class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'content/report_form.html'
    success_url = reverse_lazy('content:report_success_create')
    extra_context = {
        'title': 'Create Report',
    }

    def form_valid(self, form):
        if form.is_valid():
            content_pk = self.kwargs.get('pk')
            content = Content.objects.get(pk=content_pk)
            instance = form.save(commit=False)
            instance.user = self.request.user
            instance.content = content
            instance.slug = content.slug
            instance.save()
            return redirect('content:report_success_create')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_pk = self.kwargs.get('pk')
        content = Content.objects.get(pk=content_pk)
        context['content'] = content
        return context


def report_success_create(request):
    """
    Report creation success message
    """
    return render(request, 'content/report_success_create.html')


def content_success_create(request):
    """
    Content creation success message.
    """
    return render(request, 'content/content_success_create.html')


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
            return self.request.user.is_superuser or self.request.user.groups.filter(name='Moderators').exists()
        return False


class ReportListView(LoginRequiredMixin, ListView):
    """
    List all reports for a specific content.
    """
    model = Report
    template_name = 'content/report_list.html'
    context_object_name = 'object_list'
    extra_context = {
        'title': 'Report List',
    }

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.is_staff

    def get_queryset(self):
        content_pk = self.kwargs.get('pk')
        content_item = get_object_or_404(Content, pk=content_pk)
        queryset = super().get_queryset().filter(content=content_item)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_pk = self.kwargs.get('pk')
        content_item = get_object_or_404(Content, pk=content_pk)
        context['content'] = content_item
        context[
            'title'] = f'Reports for Article: {content_item.category}/{content_item.title}/{content_item.author.nickname}'
        return context


class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'content/report_detail.html'
    extra_context = {
        'title': 'Report Detail',
    }

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.is_staff


class BecomeAuthorView(LoginRequiredMixin, View):
    """
    Creating an instance of the Author class for a user.
    """

    def post(self, request, *args, **kwargs):
        user = request.user

        if user.is_author:
            return redirect('users:home')

        author, created = Author.objects.get_or_create(user=user)

        user.is_author = True
        user.save()

        return redirect('content:an_author')


def an_author(request):
    """
    Message about successful becoming an author.
    """
    return render(request, 'content/an_author.html')


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


class AuthorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('content:author_list')
    permission_required = 'content.delete_author'

    def test_func(self):
        if super().has_permission():
            return self.request.user.is_superuser or self.request.user.groups.filter(name='Moderators').exists()
        return False


def author_content(request, pk):
    author_item = Author.objects.get(pk=pk)
    context = {
        'object_list': Content.objects.filter(author=author_item),
        'author': author_item.pk,
        'title': f'All content of {author_item.nickname}',
    }
    return render(request, 'content/author_content.html', context)
