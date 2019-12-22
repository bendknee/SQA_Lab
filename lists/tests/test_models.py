from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.datetime_safe import datetime

from lists.models import Item


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_epoch = datetime.now()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_epoch = datetime.now()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertAlmostEqual(first_saved_item.creation_time.timestamp(), first_epoch.timestamp(), places=3)

        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertAlmostEqual(second_saved_item.creation_time.timestamp(), second_epoch.timestamp(), places=3)

    def test_cannot_save_empty_list_items(self):
        item = Item(text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
