from django.test import TestCase
from django.utils.html import escape

from lists.models import Item


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_shows_developer_bio(self):
        name = "Benny William Pardede"
        npm = "1606917550"
        role = "trequartista"

        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.strip().startswith('<html>'))
        self.assertIn(name, html)
        self.assertIn(npm, html)
        self.assertIn(role, html)
        self.assertTrue(html.strip().endswith('</html>'))

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

    def test_display_comment_if_empty_todo_list(self):
        response = self.client.get('/')
        self.assertIn('If a trequartista is doing nothing on an attack, then they have failed',
                      response.content.decode())

    def test_displayed_comment_for_each_time_new_todo_item_is_added(self):
        Item.objects.create(text='item 1')
        response = self.client.get('/')
        self.assertIn('A trequartista always check more things to do than losing its man marker',
                      response.content.decode())

        Item.objects.create(text='item 2')
        response = self.client.get('/')
        self.assertIn('A trequartista always check more things to do than losing its man marker',
                      response.content.decode())

        Item.objects.create(text='item 3')
        response = self.client.get('/')
        self.assertIn('A trequartista always check more things to do than losing its man marker',
                      response.content.decode())

        Item.objects.create(text='item 4')
        response = self.client.get('/')
        self.assertIn('A trequartista always check more things to do than losing its man marker',
                      response.content.decode())

        Item.objects.create(text='item 5')
        response = self.client.get('/')
        self.assertIn("There are no such thing as too much to do for a trequartista. "
                      "They are the attack organizer after all",
                      response.content.decode())

        Item.objects.create(text='item 6')
        response = self.client.get('/')
        self.assertIn("There are no such thing as too much to do for a trequartista. "
                      "They are the attack organizer after all",
                      response.content.decode())

        Item.objects.create(text='item 7')
        response = self.client.get('/')
        self.assertIn("There are no such thing as too much to do for a trequartista. "
                      "They are the attack organizer after all",
                      response.content.decode())

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/', data={'item_text': ''})
        self.assertEqual(Item.objects.count(), 0)
