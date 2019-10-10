# 1606917550-practice

SQA 2019 Exercise by 1606917550

Find the webpage [here](https://sqa-exercise.herokuapp.com/)

## Exercise 3 Story

### Test Isolation Process
Before exercise 3, or in particular before reaching chapter 6 of the [reference book](https://obeythetestinggoat.com),
all unit test does its job properly without disturbing the real, production database. It seems like that the unit test saves
a row to the to-do list table, but in the end of test suite, developers wouldn't find any of the saved rows in the website.
This is due to Django's `unittest` library which always generates a new, dummy, database each time a test suite (that extends
their library) is being executed, then flushes it to the void once it terminates.
But this is not the case with functional tests (FT).

FTs in general are indeed meant to test the end-to-end
 functionality of the said software to give an image of the perspective of the end user. Logically speaking, FTs should be run through a
 legitimate, fully deployed software a.k.a production software. And where does deployed software saves its data?
 In the production database of course, but this is where the problem arises. Each time a FT is executed, especially FTs
 that test the input-output behavior of a software, the input that is injected in automatically by the FT is being saved
 in the production database. This means when an user opens the deployed software, the input variable authored by the FT
 would still exist there, possibly disturbing every users intended utilization of the said software.
 
 That is why, on this exercise, FTs are being refactored, so that each run of test is isolated from the original architecture
 of the deployed software. Django's library family of tests provides the solution to generate dummy database when executing
 its test suites. Even the dev now doesn't have to turn up the server when executing the FT because the server itself is
 being quarantined by the test; LiveServerTestCase for that matter.
 
 ### Design changes
 Dev refactors the helper function `check_for_row_in_list_table` to extend the ability of implicit wait instead of explicit wait. 
 ```diff
[...]
    def tearDown(self):
        self.browser.quit()
    
+   def wait_for_row_in_list_table(self, row_text):
+       start_time = time.time()
+       while True:
+           try:
+               table = self.browser.find_element_by_id('id_list_table')
+               rows = table.find_elements_by_tag_name('tr')
+               self.assertIn(row_text, [row.text for row in rows])
+               return
+           except (AssertionError, WebDriverException) as e:
+               if time.time() - start_time > self.MAX_WAIT:
+                   raise e
   
-   def check_for_row_in_list_table(self, row_text):
-       table = self.browser.find_element_by_id('id_list_table')
-       rows = table.find_elements_by_tag_name('tr')
-       self.assertIn(row_text, [row.text for row in rows])

[...]
```
All `time.sleep` function is removed, but it's recommended to test the behavior change immedately with the helper function.
Because, for random occasions, the FT engine would slow down thus still loading the page when finding the element for `inputbox`.
Hence throwing unexpected 'ElementNotFound' error. The helper function is a workaround to stop for a second so the inputbox
element would surely exist for the next action(s).

For example:
```diff
[...]
        # Eventually Benny's to-do list grows, he types in 3 more to-do items
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Practice pinpoint shooting')
        inputbox.send_keys(Keys.ENTER)
-       time.sleep(1)
+       self.wait_for_row_in_list_table('3: Practice pinpoint shooting')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Watch fb_insight weekly play analysis')
        inputbox.send_keys(Keys.ENTER)
-       time.sleep(1)
+       self.wait_for_row_in_list_table('4: Watch fb_insight weekly play analysis')

[...]
```

## Exercise 4 Story

### Code Changes
Exercise 4 is all about styling. The software doesn't increment in terms of features at all. But the FT has some new
improvements to respond the requirements of html styling; with css just to make things simple. So we have done here is add
one specific FT test to check whether our elements (inputbox, motivation comment, table) is aligned nicely in the middle.

```diff
+   def test_layout_and_styling(self):
+       # Benny goes to the home page
+       self.browser.get(self.live_server_url)
+       self.browser.set_window_size(1024, 768)

+       # He notices the input box is nicely centered
+       inputbox = self.browser.find_element_by_id('id_new_item')
+       self.assertAlmostEqual(
+           inputbox.location['x'] + inputbox.size['width'] / 2,
+           512,
+           delta=10
+       )

+       # He also notices the motivational comment which is proportionally placed in the middle
+       comment = self.browser.find_element_by_id('motivation_comment')
+       self.assertAlmostEqual(comment.size['width'], inputbox.size['width'], delta=5)

+       # He starts a new list and sees the table is nicely centered there too
+       inputbox.send_keys('testing')
+       inputbox.send_keys(Keys.ENTER)
+       self.wait_for_row_in_list_table('1: testing')
+       table = self.browser.find_element_by_id('id_list_table')
+       self.assertAlmostEqual(
+           table.location['x'] + table.size['width'] / 2,
+           512,
+           delta=10
+       )

    def test_can_access_homepage_view_with_fullname_innit(self):
        name = "Benny William Pardede"
        npm = "1606917550"
```

And so much more changes in `home.html`, though I think its not worth showing here since its just too much changes. Sorry!
You can check the merge request which merges `exercise/4` branch to observe the changes clearly.
