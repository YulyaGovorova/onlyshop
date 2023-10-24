from django.shortcuts import render

# def index(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         print(f'{name} ({phone}): {message}')
#     return render(request, 'catalog/index.html')
#
# def format(request):
#     if request.method == 'POST':
#         button = request.POST.get('button')
#         print(f'{button}')
#     return render(request, 'catalog/format.html')

def product(request):
    context = {
        'object_list': product}
    return render(request, 'catalog/product.html', context)
