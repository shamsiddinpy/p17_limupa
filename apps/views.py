from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, FormView

from apps.forms import RegisterForm
from apps.mixins import NotLoginRequiredMixin
from apps.models import Blog, Category


class BlogListView(ListView):
    paginate_by = 5
    template_name = 'apps/blogs/blog-list.html'
    queryset = Blog.objects.order_by('-id')
    context_object_name = 'blogs'

    def get_queryset(self):
        queryset = super().get_queryset()
        if search := self.request.GET.get('search'):
            return queryset.filter(name__icontains=search)
        return queryset


class BlogDetailView(DetailView):
    queryset = Blog.objects.order_by('-created_at')
    template_name = 'apps/blogs/blog-detail.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_blogs'] = self.get_queryset()[:3]
        return context


class IndexView(TemplateView):
    template_name = 'apps/index.html'


class CustomLoginView(NotLoginRequiredMixin, LoginView):
    template_name = 'apps/login.html'
    next_page = 'index_page'


class RegisterFormView(FormView):
    template_name = 'apps/login.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register_page')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
