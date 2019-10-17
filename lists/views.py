from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    items = Item.objects.all()
    motivation_comment = pick_comment(Item.objects.count())
    error = None

    if request.method == 'POST':
        item = Item.objects.create(text=request.POST['item_text'])
        try:
            item.full_clean()
            item.save()
            return redirect('/')
        except ValidationError:
            item.delete()
            error = "You can't have an empty list item"

    return render(request, 'home.html', {"error": error, 'items': items, 'motivation_comment': motivation_comment})


def pick_comment(count):
    if count >= 5:
        return "There are no such thing as too much to do for a trequartista. " \
                      "They are the attack organizer after all"
    elif 5 > count > 0:
        return "A trequartista always check more things to do than losing its man marker"
    else:
        return "If a trequartista is doing nothing on an attack, then they have failed"
