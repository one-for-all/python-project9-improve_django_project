from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import Menu, Item
from .forms import MenuForm


def menu_list(request):
    menus = Menu.objects.filter(expiration_date__gte=datetime.date.today())\
        .order_by('year', 'season', 'expiration_date').prefetch_related(
        'items')
    return render(request, 'menu/list_all_current_menus.html', {'menus':
                                                                menus})


def menu_detail(request, pk):
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try:
        item = Item.objects.prefetch_related('chef', 'ingredients').get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_detail', pk=form.instance.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(instance=menu)
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('menu_detail', pk=pk)
    return render(request, 'menu/menu_edit.html', {'form': form})
