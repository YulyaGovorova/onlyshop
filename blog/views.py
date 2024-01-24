from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, DetailView
from pytils.translit import slugify
from django.contrib.auth.mixins import PermissionRequiredMixin
from blog.models import Blog


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publication=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['title'] = context_data['object']
        return context_data

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.inc_views_count()
        post.save()
        return post


class BlogCreateView(PermissionRequiredMixin, CreateView):
    model = Blog
    fields = ('title', 'body',)
    success_url = reverse_lazy('blog:blogs')
    permission_required = 'blog.add_blog'

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    model = Blog
    fields = ('title', 'body', 'preview', 'publication')
    permission_required = 'blog.change_blog'

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blogs_item', args=[self.kwargs.get('pk')])


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blogs')
    permission_required = 'blog.delete_blog'
