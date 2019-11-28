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

## Exercise 7 Story
### Spiking
Test Driven Development has a 'quirk' regarding its rigorous discipline. Being not allowed to code anything before
writing the test becomes a problem when a developer needs to use some external software/codes for their own.
One would have no idea what to test from the external software when they even haven't figured out how to use it to their requirements.
Some trickery to deceive the Testing Goat must be done to allow devs do some 'exploration' and 'experimentation',
and that trick is called 'Spiking'.

It's obvious that a dev should do spiking outside the production code/branch main lane. On a new branch, you could do almost
anything to do some adventuring on your new dependencies. While it seems that you're breaking stuff, it's a good trade off
when you finally gain the **idea** of implementing your new stuff but keep in mind that idea is what's left after the spike is over.
All of your written codes in this spiking branch will be thrown away when de-spiking. Though keep in mind that you may also
gain nothing from a spike (not feasible, irrelevant, etc.).

### De-spiking
De-spiking, by its name, is an action of reversing the spike. You already got the idea of how to implement your requirements
using your brand new stacks, library, or third-party software. But as I mentioned, you only retrieve **only** the idea, not the code.
Those experimentation codes should be thrown away when de-spiking, except one; the test codes. It's a rule of thumb
to create functional/unit tests before a dev went de-spiking, before they forgot what is 'correct' by the spike standards.
This time though, when implementing your idea, you should return back to the ways of Testing Goat, because you're back to
writing in the production lane/code. 

## Exercise 8 Story
### Manual mocking vs. Mock libary
Doing mocking job a.k.a Monkeypathing requires you to actually type in every object, function, attribute, that you need
to replace the real thing that you don't desire to work during runtime. This requires you to copy all necessary information
when creating the mock object, parameters in a function, attributes in a class, functions in a class, parameters in a function
in a class, and so much more. Your code length would be probably exploded by the time you realized that you already made so much
mock object, presumably for just one-off usage. Thanks to Python dynamic nature, you could easily replace a class, function,
variable, within the scope of a python file, just by an assignment. ex: `accounts.views.send_email = my_mock_send_email`.

To ease your mind, every mainstream programming languages has a mocking tool library available just for you. It is meant
to simpifly all things about mocking. Using a library, you don't need to write any mock object/function anymore, as this
library already does its magic. In python, the built-in mocking tool library is called Mock by Michael Foord. It is a
really dynamic object in my opinion as it lets you use one `Mock()` object to produce function or variable, just by a
random call of that object. For example:
```python
from unittest.mock import Mock
m = Mock()
m.any_attribute
# <Mock name='mock.any_attribute' id='140716305179152'>
type(m.any_attribute)
# <class 'unittest.mock.Mock'>
m.any_method()
# <Mock name='mock.any_method()' id='140716331211856'>
m.bar.return_value = 1
m.bar(42, var='thing')
# 1
m.bar.call_args
# call(42, var='thing')
```
You really just need one `Mock()` object to get all things done. You could spawn new mock variable by `m.{your_var_name}`.
You could spawn new mock function by `m.{your_fun_name}()`. You could fixate a function's return value by
`m.{your_fun_name}.return value = {any_return_value}`. And then when you call that function it will always return that same value.
Mock also remembers every function call, and what arguments were used in that call by `m.{your_fun_name}.call_args`.
Obviously keep in mind you could replace `m` with other namespace of your desire.

So you could already conclude that this awesome library had got you covered for all your mocking needs. What about the
monkeypatching that we did manually before? In Mock library, we do every patching with a spesific decorator called `patch`.
It works exactly like you did in manual monkeypatching, assigning your undesired function with a new mock object.
But this time, you don't define a mock object at all, not even doing `m = Mock()`. The only thing to do is set the `patch` decorator
above a function, whenever you want the object to be replaced at runtime. And then, put an extra argument in your function
definition. That argument becomes a `Mock()` object thanks to the decorator, and you can immediately do the things mentioned
above like every `Mock()` object. The decorator has a required parameter, which is a string that contains
the relative-python-dot-path to your function/class/variable. For example:
```python
from unittest.mock import patch

@patch('accounts.views.send_mail')
def test_mocking_mock_object_from_param(self, mock_arg_param):
    mock_arg_param.foo.return_value = "spesific_return_value"
```

### Why mocking = tightly coupled implementations
Remember why are we doing mock in the first place, because we have an external dependency that we don't want to use in our tests.
External dependency always relates to third-party API, which usually already had a hefty chunk of ready-to-use functions/interfaces.
It is important to remember that these third-party APIs may have several methods to accomplish a certain goal. For example,
given in the book, when we want to add Django messages to our response, you could do so by two different methods. Either 
you call `messages.add_message(SUCCESS, {msg})` or just `messages.success({msg})`. These two implementations produces the same
output, but when you really have to mock, you can only patch **one of them**, and now you are binded to a specific implementation.
Your real implementation now is somehow restricted, since your mock object is currently copying a specific method, its name, its
arguments, and perhaps its return values. You are now helpless but to comply to that specific way of implementation.
For example look at these two test functions:
```python
def test_sends_mail_to_address_from_post(self):
    self.send_mail_called = False

    def fake_send_mail(subject, body, from_email, to_list):
        self.send_mail_called = True
        self.subject = subject
        self.body = body
        self.from_email = from_email
        self.to_list = to_list

    accounts.views.send_mail = fake_send_mail

    self.client.post('/accounts/send_login_email', data={
        'email': 'benny.william@example.com'
    })

    [...]
```
`send_mail` was originally a built-in Django function that has obvious external side effect; sending a real email. Here
we assumed that `send_mail` function accepts exactly 4 arguments, `subject`, `body`, `from_email`, `to_list`, in that particular
order. Then after you read further the docs, you realize that there were optional key word arguments that `send_mail` accepts.
To use that kwargs, you also have to update your mock function since it absolutely didn't accepts any more arguments. Or else,
the test will absolutely fail. You are now obliged to comply to your own mock object, rather that your mock object complying
to your desired implementation.

This situation is what we call "tightly coupled with the implementation". Keep in mind of a rule of thumb that it's better to
test behaviour rather the implementation details. We test by giving a set of input and checking a set of output with a 
set of expectations. While mocks are powerful to neutralize undesired external side-effects, they often end up making you write
tests that checks 'how to implement' rather than 'what output to expect'.

## Exercise 9 Story
### 18.3 FT vs. 20.1 FT
In chapter 18, we added a new feature to our To-Do List website which enable users to authenticate themselves. Back then, when writing our FT
for testing the authentication process, we wrote a test which simulates the whole process of users logging in/out to/from the website.
Percival named it the 'login dance', where a FT comprises typing an email to a form, take one email from Django's outbox queue
(mail.outbox) just to click a login url, checking the navbar to make sure user is logged in, and finally logging out again.

In chapter 20, we found a way to bypass the whole authentication process by utilizing a backdoor in Django's Session manager.
Through this backdoor we can inject a legitimate user to the session database. Then that database will return a Session object which
holds a session key that we can inject to the Selenium browser as a new cookie. That way, the Selenium browser will store a cookie
that helps Django identify an authenticated session, and eventually an authenticated user.

Furthermore, we wrote two helper functions which is analogous to `wait_for` helper function we had created many exercises ago.
The functions `wait_to_be_logged_in` and `wait_to_be_logged_out` basically told the browser to wait because we're trying to
look for the indicators of an authenticated session or unauthenticated session: the texts on the navbar.
We also made this functions also for the sake of de-duplication. But these two is not what we're covering when discussing
about bypassing authentication process.

**So why our new FT code works better?** In further development, we can assume that someday we want to build new features that extends
from this authentication use case. And as usual, when we need to develop a new 'feature', we must write the FT first.
But because our new feature needs a authenticated user as a precondition, we must write out the whole login dance first
before writing the actual test case. Duplication issue will be coming quick before we knew it, and this is where the authentication
bypass method `create_pre_authenticated_session` steps up as a solution. It saves runtime and saves code lines aswell.
Test data that populates the database to fulfill precondition is called **test fixture**. What happens in function
`create_pre_authenticated_session` is basically injecting one test fixture to the session database and to the browser cookie.

But keep in mind that there's some degree of limitations in this shortcut. Percival mentioned that this shortcut works because
we're using the `LiveServerTestCase` library, so both User and Session entities end up in the same database as the view server.
Percival warned this as a heads-up for us to not overdoing de-duplication in FTs. Because FTs may catch unpredictable
interactions between different parts (features) of one's application. We have to make sure shortcuts or cheats doesn't 
conflict with the real use case in our 'world'. But since this shortcut is simulating what is really happening in our browser,
storing sessions in cookies, this shortcut becomes justifiable.
