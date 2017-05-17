# CSUIBot

<<<<<<< HEAD
<<<<<<< HEAD
[![build status](https://gitlab.com/CSUI-AdvProg-2017/project-b/csui-bot-2/badges/master/build.svg)](https://gitlab.com/CSUI-AdvProg-2017/project-b/csui-bot-2/master)
[![coverage report](https://gitlab.com/CSUI-AdvProg-2017/project-b/csui-bot-2/badges/master/coverage.svg)](https://gitlab.com/CSUI-AdvProg-2017/project-b/csui-bot-2/commits/master)
=======
# Background
>>>>>>> 59a51601dabbe8d3b24f291354d0d6a0623b1241

Similar to: #102

Learning by googling some time faster than reading a book. however, googling for basic courses is not really efficient and effective because they usually give more answer than we need. Most of the time, for basic courses such as Discrete Math or Linear Algebra, following the lecture notes and the given text book is better. 

It is also probably helpful to have terminology references while discussing some concept with your friend.

# Description

N/A
 
# Definition of Done

- [ ] Create a database of dictionary in JSON format as a flat text file.  
    - The format should at least consists of:
    ```
    Course (e.g Discrete Math),
    Keyword (e.g. relation), 
    Definition (e.g. definition of relation), 
    Example (e.g example of some relation), 
    Ref (e.q. chapter in the text book for further reading),
    Problem (e.g. example of related problem in exam or quiz)
    ```
- [ ] Provide command to query. For example: `/tellme relation`
    - The bot will nicely render the answer by using layout, colour and typesetting appropriately. 
    If the data about relation is not available, the bot answer nicely, for example: 
    No one has told me about relation, please ask someone to add it in our knowledge base.
- [ ] WIP contained in a branch and tracked in GitLab repository
- [ ] Created or worked a module specific for containing functionalities related to this user story
- [ ] Wrote stubs & unit tests
- [ ] Test coverage >= 70%
- [ ] Provided error handling for boundary cases and other exceptional cases
- [ ] Build passed (i.e. not failed)
- [ ] Have tested the working build on Heroku instance
=======
[![build status](https://gitlab.com/CSUI-AdvProg-2017/project-b/csui-bot-2/badges/master/build.svg)](https://gitlab.com/CSUI-AdvProg-2017/project-b/csui-bot-2/master)
[![coverage report](https://gitlab.com/CSUI-AdvProg-2017/project-b/csui-bot-2/badges/master/coverage.svg)](https://gitlab.com/CSUI-AdvProg-2017/project-b/csui-bot-2/commits/master)

## How the Bot Works

There are two ways for the bot to get updates from Telegram: long
polling and webhook. In this project, we are using webhook. Using
`setWebhook` method provided by Telegram API, we can associate a bot
with a webhook URL so that whenever there is an update (a new message,
a new member joining a group, etc.), Telegram will send the update data
to the webhook URL in a JSON format. The general steps are as follows:

1. An update occurs in a chat or group of which the bot is a member.
2. Telegram sends the update to the bot's webhook URL as HTTP POST
request containing JSON data.
3. Server makes a request to Telegram via its Bot API to initiate
bot's response, while responding with 200 status to the HTTP POST
request made by Telegram.

More detailed information can be found [here](https://core.telegram.org/bots/api#getting-updates).

## Development Guide

### How to set up your machine

1. Setup your Python virtual environment using [venv](https://docs.python.org/3/library/venv.html)
as you did in [week 8 tutorial](https://gitlab.com/CSUI-AdvProg-2017/lab-exercises/blob/master/week_8/README.md).
If you use PyCharm, you may want to configure it to recognize your virtual environment too.
2. Navigate to the directory where you've cloned this repo and create a
virtual environment under the `env` directory. Then, activate the virtual environment.
3. Still in the directory where you've cloned this repo, install all its dependencies.

    ```bash
    pip install -r requirements.txt
    ```

    Dependencies are all listed in `requirements.txt`. To re-generate
    this file (after you've installed new packages), simply run
    `pip freeze > requirements.txt`. For Linux users, if you have a
    problem installing the dependencies, install `python3-dev` or
    `python3-devel` system package first.
4. Create `.env` file under the project root directory. It contains the
configuration variables for the application. Sample `.env` file can be
found in `.env.example`.
5. Run the app

    ```bash
    python manage.py runserver
    ```
6. The app is now running! To check that the bot is actually running,
try to send a GET request to it, for instance:

    ```bash
    curl http://127.0.0.1:5000
    ```

    or open `http://127.0.0.1:5000` from your browser. You should get a
    response that says:

    ```bash
    Bot is running
    ```

### How to run the tests/linters

1. Make sure you already installed [pytest][pytest] and [flake8][flake8].
Both are listed in `requirements.txt` so if you followed the instructions
to setup your machine above then they should already be installed.
2. Put an `.env` file under your `tests` directory. This file could be
identical to the one in project root directory or you may also set some
environment variables for testing to your liking.
3. You can run the tests and linters with `python manage.py test` and
`python manage.py lint` respectively.
4. To run both linters and tests in one command, you can use
`python manage.py check`. This is useful to check your code before making
a merge request.
5. For more info on what you can do with `manage.py`, run
`python manage.py --help`.

[pytest]: http://pytest.org/latest/
[flake8]: https://pypi.python.org/pypi/flake8

### How to Contribute

If you want to write new features to CSUIBot or fix bugs, that's great! Here is a step-by-step guide to contribute to CSUIBot's development.

#### General Flow

1. You need an issue on GitLab about your contribution. This can be a
bug report (in which case your contribution is the bug fix) or feature
suggestion (in which case your contribution is the implementation).
2. Make sure that you are in `master` branch by running `git status`.
If not, run `git checkout master` to move to `master` branch.
3. Create a new branch on which you write your code. Use any branch
name as you wish. For example, `cool-feature`:

    ```bash
    git checkout -b cool-feature
    ```
4. Implement your contribution in the branch.
5. Periodically, and after you committed your changes, pull the latest
changes from master and merge the changes to your working branch. This
ensures your branch is always up-to-date with the origin.

    ```bash
    git pull origin master
    git merge master
    ```

    Fix any conflicts that may arise.
6. After you really finished writing the code, commit your changes. You
may create one or more commits.
7. Push the feature branch to `origin`:

    ```bash
    git push origin cool-feature
    ```
8. Create a new merge request on GitLab for `cool-feature` branch to be
merged to `master`. Assign your group supervisor as the assignee of the
new merge request.
9. Wait for other project members and class instructors to review your
contribution.
10. If they approve your contribution, congrats! Your contribution may
be merged to master. First, don't forget pull latest changes from master
and merge the changes to your working branch.

    ```bash
    git pull origin master
    git merge master
    ```

    Again, fix any conflicts that may arise and push the merge commits.
11. Ask the class instructors to merge your contribution to master.
12. After your contribution is merged, you may safely delete your feature branch:

    ```bash
    git branch -D cool-feature
    ```

    Also delete your feature branch on origin from Gitlab.

    ```bash
    git push origin :cool-feature
    ```
13. Done!
>>>>>>> 5537b61e32a78c48f67fb1a4c59fe9dbfaaf6d06
