from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from .forms import ProductForm, CommentForm, SearchForm
from .models import Product, Comment
from django.contrib.auth.models import User
from django.http import HttpResponse


class ProductListView(ListView):
    model = Product
    context_object_name = 'all_the_products'  # Default: object_list
    template_name = 'product-list.html'  # Default: book_list.html


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'that_one_product'  # Default: book
    template_name = 'product-detail.html'  # Default: book_detail.html


def product_detail(request, **kwargs):
    product_id = kwargs['pk']
    product = Product.objects.get(id=product_id)
    comment_id = kwargs['pk']
    comment = Comment.objects.get(id=comment_id)

    # Add comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.user = request.user
        form.instance.product = product
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    if(product.get_upvotes_count() > 0):
        vote = (product.get_upvotes_count() * 100 / (product.get_upvotes_count() + product.get_downvotes_count()))
    else:
        vote = 0
    comments = Comment.objects.filter(product=product)
    context = {'that_one_product': product,
               'comments_for_that_one_product': comments,
               'upvotes': product.get_upvotes_count(),
               'downvotes': product.get_downvotes_count(),
               #'like': comment.get_upvotes_count(),
               #'dislike': comment.get_downvotes_count(),
               #'report': comment.get_report_count(),
               'vote': vote,

               'comment_form': CommentForm}
    return render(request, 'product-detail.html', context)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    form_class
    context_object_name = 'products'
    template_name = 'product-create.html'  # Default: book_form.html
    success_url = reverse_lazy('product-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def model_form_upload(request):
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = ProductForm()
        return render(request, 'product-list.html', {
            'form': form
        })

    def image_upload_view(request):
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                # Get the current instance object to display in the template
                img_obj = form.instance
                return render(request, 'product-create.html', {'form': form, 'img_obj': img_obj})
        else:
            form = ProductForm()
        return render(request, 'product-create.html', {'form': form})


def vote(request, pk: str, up_or_down: str):
    product = Product.objects.get(id=int(pk))
    user = request.user
    product.vote(user, up_or_down)
    return redirect('product-detail', pk=pk)


def product_search(request):
    if request.method == 'POST':
        search_string_user = request.POST['title']
        products_found = Product.objects.filter(title__contains=search_string_user)
        search_string_title = request.POST['title']
        if search_string_title:
            products_found = products_found.filter

        form_in_function_based_view = SearchForm()
        context = {'form': form_in_function_based_view,
                   'products_found': products_found,
                   'show_results': True}
        return render(request, 'product-search.html', context)

    else:
        form_in_function_based_view = SearchForm()
        product = Product.objects.all()
        context = {'form': form_in_function_based_view,
                   'products_found': product,
                   'show_results': True}
        return render(request, 'product-search.html', context)


def product_list(request):
    product = Product.objects.all()
    if request.method == 'POST':
        if 'type' in request.POST:
            search_string_user = request.POST['type']
            products_found = Product.objects.filter(type__contains=search_string_user)
            search_string_title = request.POST['type']
            if search_string_title:
                products_found = products_found.filter

            form_in_function_based_view = SearchForm()
            context = {'form': form_in_function_based_view,
                       'products_found': products_found,
                       'show_results': True}
            return render(request, 'product-list.html', context)
        if 'title' in request.POST:
            search_string_user = request.POST['title']
            products_found = Product.objects.filter(title__contains=search_string_user)
            search_string_title = request.POST['title']
            if search_string_title:
                products_found = products_found.filter

            form_in_function_based_view = SearchForm()
            context = {'form': form_in_function_based_view,
                       'products_found': products_found,
                       'show_results': True}
            return render(request, 'product-list.html', context)
        if 'user' in request.POST:
            search_string_user = request.POST['user']
            print(search_string_user)
            products_found = Product.objects.filter(user_id__exact=search_string_user)
            search_string_title = request.POST['user']
            if search_string_title:
                products_found = products_found.filter

            form_in_function_based_view = SearchForm()
            context = {'form': form_in_function_based_view,
                       'products_found': products_found,
                       'show_results': True}
            return render(request, 'product-list.html', context)


    else:
        form_in_function_based_view = SearchForm()
        context = {'form': form_in_function_based_view,
                   'products_found': product,
                   'show_results': True}
        return render(request, 'product-list.html', context)

def like(request, pk: int, comment_pk: int, Like_or_not: str):
    comment = Comment.objects.get(id=comment_pk)
    user = request.user
    comment.like(user, Like_or_not)
    return redirect('product-detail', pk=pk)


def report(request, pk: int, comment_pk: int, report: str):
    comment = Comment.objects.get(id=comment_pk)
    user = request.user
    comment.report(user, report)
    return redirect('product-detail', pk=pk)
