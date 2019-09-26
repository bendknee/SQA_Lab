from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    if Item.objects.count() >= 5:
        comment = "There are no such thing as too much to do for a trequartista. " \
                      "They are the attack organizer after all"
    elif 5 > Item.objects.count() > 0:
        comment = "A trequartista always check more things to do than losing its man marker"
    else:
        comment = "If a trequartista is doing nothing on an attack, then they have failed"

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items, 'motivation_comment': comment})
