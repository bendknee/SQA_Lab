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

## Exercise 5 Story
### Clean Code x TDD
When taking the Software Project course on the first half of 2019, I was required to make a blog to write my thoughts on
several topics of software engineering. And apparently one of those topics are about TDD. [Quoting myself](https://medium.com/ppl-d7-fasilkom-ui/test-drive-782524fec72d),
in TDD, Refactor means “fixing your code quality that maybe has been abandoned due to only focusing on making the test pass, without making the test fail”.
Building a software often requires a team, it’s not only you who determine tests, who implement functions.
To enhance code understanding between developers, all of the members have to ensure good code quality in their deliverables.
To improve code quality, developers often recognize code smells and fix it so it will be clean. And these code smell removals
are heavily related to Clean Code.

Although now after I looked back at my blog, I realized that what I wanted to push to the readers is to refactor ASAP.
**No refactor, no deliver**. That's just in contrast to Mr. Percival who confessed that refactoring often took months 
for him to realize that he really have to do refactoring in his work.
And now I have to confess too that I agree with him. I had to eat my own words when working on a real industry setting as an intern.
These refactor-immediately mindset has got into me as a some sort of paranoia. I'm aware the unittest passes but also
itching for more optimization, more clean writings; where it's not really necessary. I realized that this Refactor phase in TDD
is just trying to tell us that anyone should feel free to refactor whenever they're not in a working state; currently in Green phase.
But also make sure your refactoring activity doesn't bring you back to Red!
Because the only time a code state could go back to the Red phase is when you're adding new unittests.

### Test Organization
The point here on separating test classes on different files is the common sense that one source code file is just
unnavigable if that file has too many lines/functions/classes bulked in together. Especially when there are so much classes
that have no relation at all, eventually degrading the initial meaning of the file name. Test always grows in TDD, so
cluttering test classes in one test file is just an unavoidable consequence. But to reduce damage from this consequence, one dev could
do some test organization so that devs could navigate on file names instead of class names inside one possibly unrelated file.

On my opinion though, organizing things is just a general intuitive solution to make things tidier.
It's always nice to have a tidy arrangement of things. Tidy book shelf is nice to find books,
tidy shoe racks are nice to find shoes, and Mr. Percival maybe thought it applies to tidy directories too.
