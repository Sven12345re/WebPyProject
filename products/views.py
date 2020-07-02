from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from .forms import ProductForm,CommentForm
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

    # Add comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.user = request.user
        form.instance.product = product
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    comments = Comment.objects.filter(product=product)
    context = {'that_one_product': product,
               'comments_for_that_one_product': comments,
               'upvotes': product.get_upvotes_count(),
               'downvotes': product.get_downvotes_count(),
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