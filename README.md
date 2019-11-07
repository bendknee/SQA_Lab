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

## Exercise 6 Story
#### Mutant 6.1: Relational Operator Replacement
```diff
[...]

def pick_comment(count):
-   if count >= 5:
+   if count == 5:
        return "There are no such thing as too much to do for a trequartista. " \
                      "They are the attack organizer after all"
    elif 5 > count > 0:
        return "A trequartista always check more things to do than losing its man marker"
    else:
        return "If a trequartista is doing nothing on an attack, then they have failed"
```
#### Mutant 6.2: Relational Operator Replacement
```diff
def home_page(request):
    items = Item.objects.all()
    motivation_comment = pick_comment(Item.objects.count())
    error = None

-   if request.method == 'POST':
+   if request.method != 'POST':
        item = Item.objects.create(text=request.POST['item_text'])
        try:
            item.full_clean()
            item.save()
            return redirect('/')
        except ValidationError:
            item.delete()
            error = "You can't have an empty list item"

    return render(request, 'home.html', {"error": error, 'items': items, 'motivation_comment': motivation_comment})

[...]
```

These two mutants had different conclusions, given the test cases that we own right now.
Mutant 6.1 survived through all test cases while **mutant 6.2 has been killed for just being an incompetent mutant**.
Being an incompetent mutant means that a mutant infects a program just to trigger overt runtime errors/exceptions during execution.

Mutation testing for Mutant 6.1 
```text
System check identified no issues (0 silenced).
..................
----------------------------------------------------------------------
Ran 18 tests in 89.787s

OK
Destroying test database for alias 'default'...
```

Mutation testing for Mutant 6.2
```text
System check identified no issues (0 silenced).
..FEEEEE.EFEFEFEEE
----------------------------------------------------------------------
Ran 18 tests in 54.819s

FAILED (failures=4, errors=11)
Destroying test database for alias 'default'...
```

To kill mutant 6.1, I modified an existing test case (method) that tests the displayed comment when there are greater equal than
five to-do list items on the table. The method in subject is `test_display_comment_if_todo_items_greater_equal_than_five`
inside test_views.py

```diff
def test_display_comment_if_todo_items_greater_equal_than_five(self):
    Item.objects.create(text='item 1')
    Item.objects.create(text='item 2')
    Item.objects.create(text='item 3')
    Item.objects.create(text='item 4')
    Item.objects.create(text='item 5')
+   Item.objects.create(text='item 6')

    response = self.client.get('/')
    self.assertIn("There are no such thing as too much to do for a trequartista. "
                  "They are the attack organizer after all",
                  response.content.decode())
```

Now mutant 6.1 is dead, thanks to that test case modification
```text
System check identified no issues (0 silenced).
....F.............
======================================================================
FAIL: test_display_comment_if_todo_items_greater_equal_than_five (lists.tests.test_views.HomePageTest)
[...]

----------------------------------------------------------------------
Ran 18 tests in 120.640s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

The test method here is modified without changing the correctness, but this time the mutant won't survive.
Before, I was naive assuming that a test case with `equal than` premise should be enough to test the correctness
of a `greater equal than` premise.

#### Mutation Testing Tool
I chose Cosmic-Ray by Austin Bingham to help me mutating views.py with all the possible mutation a Python code
could experience. And it turns out that my current test cases missed out some mutations.

```text
[...]
7dcb1731191b4aa0922bfb1c39303523 lists/views.py core/NumberReplacer 5
worker outcome: normal, test outcome: killed
total jobs: 33
complete: 33 (100.00%)
survival rate: 21.21%
```

I've got about 7 mutations that survived my test cases, and several of those survivors mutates my program in a similar fashion.
_I didn't show all the mutants here_.

```diff
--- mutation diff ---
--- alists/views.py
+++ blists/views.py

def pick_comment(count):
-    if count >= 5:
+    if count == 5:
+    if count >= 4:
        return "There are no such thing as too much to do for a trequartista. " \
                      "They are the attack organizer after all"
-    elif 5 > count > 0:
+    elif 6 > count > 0:
+    elif 4 > count > 0:
+    elif 5 > count > 1:
        return "A trequartista always check more things to do than losing its man marker"
    else:
        return "If a trequartista is doing nothing on an attack, then they have failed"
```

Each relational operator is being mutated to all its counterparts, and I already had so many lying in my source code.
But rather than tweaking the source code we must face the fact that some major changes should be done in our tests,
and the focus is on the `display comment` feature.

What I did is combining two test cases that test two specifications of the feature, testing display comment when there are
to-do list items but less than five and when there are greater than equal five to-do list items. In short I combined the
essence of test case `test_display_comment_if_todo_items_less_than_five` and `test_display_comment_if_todo_items_greater_equal_than_five`
to become just one generalized test case `test_displayed_comment_for_each_time_new_todo_item_is_added`. It checks the comment
**every time** a to-do list item is added. It stops at 6 items for obvious reasons.

```python
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
```

When I run cosmic-ray again, it tells me that my new test suites are killing more mutants

```text
[...]
total jobs: 33
complete: 33 (100.00%)
survival rate: 18.18%
```

But improving from 21 to 18 percent means that I succeeded killing only one survivor from previous round, that's not relieving news.
So I checked what kind of mutants that went through.

```diff
--- mutation diff ---
--- alists/views.py
+++ blists/views.py

def pick_comment(count):
    if count >= 5:
        return "There are no such thing as too much to do for a trequartista. " \
                      "They are the attack organizer after all"
-    elif 5 > count > 0:
+    elif 5 != count > 0:
+    elif 5 > count != 0:
+    elif 5 >= count > 0:
+    elif 5 is not count > 0:
+    elif 6 > count > 0:
        return "A trequartista always check more things to do than losing its man marker"
    else:
        return "If a trequartista is doing nothing on an attack, then they have failed"
```

It seems that mutations like `5 >= count > 0` and `6 > count > 0` survives because
the program execution won't simply get to that point when `count` is >= 5. Moreover, the if-clause has too many operators that
the mutation tool starts making odd, trivial mutations like `elif 5 != count > 0`, `elif 5 > count != 0`, or `elif 5 is not count > 0`

I'm starting to figure what's going on. I have to reduce those symbols somehow. And I thought it can be done by reconstructing
the if-clause. I remembered a rule-of-thumb that the most tight (edge) case should always be on top of a if-clause.
We have three conditions of `count`: 0, 1-4, and 5-∞. The most tight range here is 0, then 1-4, and then >= 5.
So then I rearranged the if-clause to this

```python
def pick_comment(count):
    if count == 0:
        return "If a trequartista is doing nothing on an attack, then they have failed"
    if count < 5:
        return "A trequartista always check more things to do than losing its man marker"
    else:
        return "There are no such thing as too much to do for a trequartista. " \
                      "They are the attack organizer after all"    
```
You can witness that there are much less relational symbols already in this function. And to prove my hypothesis, I ran cosmic-ray
once again and obtain this result

```text
[...]
total jobs: 24
complete: 24 (100.00%)
survival rate: 8.33%
```

I guess I'm just bad at designing program branches.

The total mutations reduced, the survival rate reduced even more, dropping from 18 to just 8.
The only surviving mutant is an arguably bizarre one though.
I don't think I can do anything to prevent this, how else would you compare strings in Python?

```diff
--- mutation diff ---
--- alists/views.py
+++ blists/views.py
@@ -9,7 +9,7 @@
     motivation_comment = pick_comment(Item.objects.count())
     error = None
 
-    if request.method == 'POST':
+    if request.method >= 'POST':
         item = Item.objects.create(text=request.POST['item_text'])
         try:
             item.full_clean()
```
