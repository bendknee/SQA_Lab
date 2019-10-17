from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class StylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Benny goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # He also notices the motivational comment which is proportionally placed in the middle
        comment = self.browser.find_element_by_id('motivation_comment')
        self.assertAlmostEqual(comment.size['width'], inputbox.size['width'], delta=5)

        # He starts a new list and sees the table is nicely centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        table = self.browser.find_element_by_id('id_list_table')
        self.assertAlmostEqual(
            table.location['x'] + table.size['width'] / 2,
            512,
            delta=10
        )
