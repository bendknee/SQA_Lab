import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class HomePageTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_access_homepage_view_with_fullname_innit(self):
        name = "Benny William Pardede"
        npm = "1606917550"
        role = "trequartista"

        # Benny needs to show make an introductory homepage of himself
        # Benny had filled the landing page with internal gags within himself
        # Benny needs help

        # He opens the browser to open the page
        self.browser.get('http://localhost:8000')

        # He notices the page title goes 'Homepage'
        self.assertEquals('Homepage', self.browser.title)

        # There's his birth name
        self.assertIn(name, self.browser.find_element_by_id('name').text)

        # That's just his alias
        self.assertIn(role, self.browser.find_element_by_id('alias').text)

        # His Student Id
        self.assertIn(npm, self.browser.find_element_by_id('npm').text)

    def test_homepage_can_start_a_todo_list_and_retrieve_it_later(self):
        # Benny has heard about a cool new online to-do app. He opens it to
        # list out what it needs to be a proper trequartista.
        self.browser.get('http://localhost:8000')

        # He notices a input box that invites him to write a to-do
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He also notices there's a somewhat motivational comment next to input box
        # It seems that the page knows that Benny has no to-do item submitted yet
        comment = self.browser.find_element_by_id('motivation_comment')
        self.assertEqual(comment.text, "If a trequartista is doing nothing on an attack, then they have failed")

        # He types "Practice check-in check-out" into a text box
        inputbox.send_keys('Practice check-in check-out')

        # When he hits enter, the page updates, and now the page lists
        # "1: Practice check-in check-out" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Practice check-in check-out')

        # There is still a text box inviting him to add another item. He
        # enters "Shuttle run at 5.00 PM"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Shuttle run at 5.00 PM')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on his list
        self.check_for_row_in_list_table('1: Practice check-in check-out')
        self.check_for_row_in_list_table('2: Shuttle run at 5.00 PM')

        # Benny closes the page, continues to practice

    def test_homepage_will_pop_different_comment_depending_on_todo_list_quantity(self):
        self.browser.get('http://localhost:8000')
        # Benny opens the page again, notices that the motivational comment has changed.
        # Probably because now Benny has some to-do items listed on the page.
        comment = self.browser.find_element_by_id('motivation_comment')
        self.assertEqual(comment.text, "A trequartista always check more things to do than losing its man marker")

        # Eventually Benny's to-do list grows, he types in 3 more to-do items
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Practice pinpoint shooting')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Watch fb_insight weekly play analysis')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Improve pace-change dribbling')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Now the list has exactly 5 items, 2 items from the previous session plus new fresh 3 to-do items
        self.check_for_row_in_list_table('1: Practice check-in check-out')
        self.check_for_row_in_list_table('2: Shuttle run at 5.00 PM')
        self.check_for_row_in_list_table('3: Practice pinpoint shooting')
        self.check_for_row_in_list_table('4: Watch fb_insight weekly play analysis')
        self.check_for_row_in_list_table('5: Improve pace-change dribbling')

        # Then he notices yet again the motivational comment changes. It's because he has so many
        # to-do items unfinished right now.
        comment = self.browser.find_element_by_id('motivation_comment')
        self.assertEqual(comment.text,
                         "There are no such thing as too much to do for a trequartista. "
                         "They are the attack organizer after all")


if __name__ == '__main__':
    unittest.main(warnings='ignore')
