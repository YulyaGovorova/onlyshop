from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, DetailView
from pytils.translit import slugify

from blog.models import Blog


class BlogListView(ListView):
    paginate_by = 4
    model = Blog
    extra_context = {
        'title': 'Блоги'
    }

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
        post.view_count()
        post.save()

        return post


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'body',)
    success_url = reverse_lazy('blog:blogs')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'body', 'preview', 'publication')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blogs_item', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blogs')
