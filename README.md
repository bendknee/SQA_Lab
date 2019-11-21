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
