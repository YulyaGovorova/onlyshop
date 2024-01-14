from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy

from catalog.forms import ProductForm,  VersionForm
from catalog.models import Product, Version
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from catalog.service import get_cached_categories
from config import settings


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'objects_list'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        version_list = Version.objects.all()
        context_data['formset'] = version_list
        return context_data


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(product_is_publicated=True)
        return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['title'] = context_data['object']
        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')
    permission_required = 'catalog.add_product'

    def get_initial(self):
        return {'user': self.request.user}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['category_list'] = get_cached_categories()
        return context_data


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')
    permission_required = 'catalog.delete_product'


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')
    permission_required = 'catalog.change_product'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        version_formset = inlineformset_factory(Product, Version, form=VersionForm, fields='__all__', extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = version_formset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = version_formset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

class ProductContactListView(ListView):
    model = Product
    template_name = 'catalog/contact.html'


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        send_mail(f'You have new message from {name}({phone})', message,
        settings.EMAIL_HOST_USER, ['tishyulya.1@yandex.ru'])
        print(f'You have new message from {name}({phone}): {message}')
    context = {
        'title': 'Контакты'
    }
    return render(request, 'catalog/contact.html', context)

class VersionCreateView(PermissionRequiredMixin, CreateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:index')
    permission_required = 'catalog.add_version'