from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    items = Item.objects.all()

    if request.method == 'POST':
        item = Item.objects.create(text=request.POST['item_text'])
        try:
            item.full_clean()
            item.save()
        except ValidationError:
            item.delete()
            error = "You can't have an empty list item"
            return render(request, 'home.html', {"error": error, 'items': items})
        return redirect('/')

    if Item.objects.count() >= 5:
        comment = "There are no such thing as too much to do for a trequartista. " \
                      "They are the attack organizer after all"
    elif 5 > Item.objects.count() > 0:
        comment = "A trequartista always check more things to do than losing its man marker"
    else:
        comment = "If a trequartista is doing nothing on an attack, then they have failed"

    return render(request, 'home.html', {'items': items, 'motivation_comment': comment})
