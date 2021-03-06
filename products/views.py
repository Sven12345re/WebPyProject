from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView
from .forms import ProductForm, CommentForm, SearchForm, ProductUpdateForm
from .models import Product, Comment
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView


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

    # Add comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.user = request.user
        form.instance.product = product
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    comments = Comment.objects.filter(product=product).order_by('-id')
    averageRate = comments.values('rate')
    rate_all = 0
    for rate in averageRate:
        rate_all = rate_all + rate['rate']

    if rate_all > 0:
        average = Decimal(rate_all / len(averageRate)).quantize(0, ROUND_HALF_UP)
    else:
        average = 0
    context = {'that_one_product': product,
               'comments_for_that_one_product': comments,
               'vote': vote,
               'averageRate': average,
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
    alreadyLiket = False
    for userId in comment.get_upvotes().values('user_id'):
        if user.id == userId['user_id']:
            alreadyLiket = True
            continue
    for userId in comment.get_downvotes().values('user_id'):
        if user.id == userId['user_id']:
            alreadyLiket = True
            continue

    if not alreadyLiket:
        comment.like(user, Like_or_not)

    return redirect('product-detail', pk=pk)


def report(request, pk: int, comment_pk: int, report: str):
    comment = Comment.objects.get(id=comment_pk)
    user = request.user
    alreadyReportet = False
    for userId in comment.get_report().values('user_id'):
        print(userId['user_id'])
        if user.id == userId['user_id']:
            alreadyReportet = True
            continue

    if not alreadyReportet:
        comment.report(user, report)
    return redirect('product-detail', pk=pk)


def manager_portal(request, **kwargs):
    comments = Comment.objects.all()
    products = Product.objects.all()
    context = {'comments': comments,
               'products': products}
    return render(request, 'manager-portal.html', context)


def comment_delete(request, pk):
    template = 'delete.html'
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user == request.user:

        if request.method == 'POST':
            comment.delete()
            return redirect('product-list')
        context = {"comment": comment}
        return render(request, template, context)


def comment_update(request, pk):
    template = 'product_update_form.html'
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user == request.user:
        form = CommentForm(request.POST or None, instance=comment)
        if form.is_valid():
            print("Comment")
            form.save()
            return redirect('product-list')
        context = {"form": form}
        return render(request, template, context)


def comment_delete_manager(request, pk):
    template = 'delete.html'
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_staff:
        if request.method == 'POST':
            comment.delete()
            return redirect('/product/manager')
        context = {"comment": comment}
        return render(request, template, context)


def delete_product_manager(request, pk):
    template = 'delete.html'
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_staff:
        if request.method == 'POST':
            product.delete()
            return redirect('/product/manager')
        context = {"product": product}
        return render(request, template, context)


def comment_update_manager(request, pk):
    template = 'product_update_form.html'
    comment = get_object_or_404(Comment, pk=pk)

    form = CommentForm(request.POST or None, instance=comment)
    if request.user.is_staff:
        if form.is_valid():
            form.save()
            return redirect('/product/manager')
        context = {"form": form}
        return render(request, template, context)


def edit_product_manager(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        if request.user.is_staff:
            form = ProductForm(request.POST or None, request.FILES, instance=product)
            if form.is_valid():
                form.save()
        return redirect('manager-portal')
    else:
        form = ProductUpdateForm(request.POST or None, instance=product)
    return render(request, 'add-product-photo.html', {'form': form})
