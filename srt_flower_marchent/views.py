from django.shortcuts import render, get_object_or_404, redirect

from .models import Flower
from .forms import FlowerPriceForm


def home(request):
    return render(request, 'srt_flower_marchent/home.html')


def contact(request):
    return render(request, 'srt_flower_marchent/contact.html')


def flowers_list(request):
    flowers = Flower.objects.order_by('-created_at')
    return render(request, 'srt_flower_marchent/flowers_list.html', {'flowers': flowers})


def edit_price(request, pk):
    flower = get_object_or_404(Flower, pk=pk)
    if request.method == 'POST':
        form = FlowerPriceForm(request.POST, request.FILES, instance=flower)
        if form.is_valid():
            form.save()
            return redirect('flowers_list')
    else:
        form = FlowerPriceForm(instance=flower)
    return render(request, 'srt_flower_marchent/edit_price.html', {'form': form, 'flower': flower})
