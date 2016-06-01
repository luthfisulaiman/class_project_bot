# CSUIBot

## How the Bot Works

There are two ways for the bot to get updates from Telegram: long polling and webhook. In this project, we are using webhook. Using `setWebhook` method provided by Telegram API, we can associate a bot with a webhook URL so that whenever there is an update (a new message, a new member joining a group, etc.), Telegram will send the update data to the webhook URL in a JSON format. The general steps are as follows:

1. An update occurs in a chat or group of which the bot is a member.
1. Telegram sends the update to the bot's webhook URL as HTTP POST request containing JSON data.
1. Server makes a request to Telegram via its Bot API to initiate bot's response, while responding with 200 status to the HTTP POST request made by Telegram.

More detailed information can be found [here](https://core.telegram.org/bots/api#getting-updates).

## Development Guide

### How to set up your machine

1. Setup your Python virtual environment using [venv](https://docs.python.org/3/library/venv.html) as you did in week 8 tutorial. If you use PyCharm, you may want to configure it to recognize your virtual environment too.

1. Navigate to the directory where you've cloned this repo and create a virtual environment under the `env` directory. Then, activate the virtual environment.

1. Still in the directory where you've cloned this repo, install all its dependencies.

    ```bash
    pip install -r requirements.txt
    ```

    Dependencies are all listed in `requirements.txt`. To re-generate this file (after you've installed new packages), simply run `pip freeze > requirements.txt`. For Linux users, if you have a problem installing the dependencies, install `python3-dev` or `python3-devel` system package first.

1. Create `.env` file under the project root directory. It contains the configuration variables for the application. Sample `.env` file can be found in `.env.example`.

1. Run the app

    ```bash
    python manage.py runserver
    ```

1. The app is now running! To check that the bot is actually running, try to send a GET request to it, for instance:

    ```bash
    curl http://127.0.0.1:5000
    ```

    or open `http://127.0.0.1:5000` from your browser. You should get a response that says:

    ```bash
    Bot is running
    ```

### How to run the tests/linters

1. Make sure you already installed [pytest][pytest] and [flake8][flake8]. Both are listed in `requirements.txt` so if you followed the instructions to setup your machine above then they should already be installed.

1. Put an `.env` file under your `tests` directory. This file could be identical to the one in project root directory or you may also set some environment variables for testing to your liking.

1. You can run the tests and linters with `python manage.py test` and `python manage.py lint` respectively.

1. To run both linters and tests in one command, you can use `python manage.py check`. This is useful to check your code before making a merge request.

1. For more info on what you can do with `manage.py`, run `python manage.py --help`.

[pytest]: http://pytest.org/latest/
[flake8]: https://pypi.python.org/pypi/flake8

### How to Contribute

If you want to write new features to CSUIBot or fix bugs, that's great! Here is a step-by-step guide to contribute to CSUIBot's development.

#### General Flow

1. You need an issue on Pivotal Tracker about your contribution. This can be a bug report (in which case your contribution is the bug fix) or feature suggestion (in which case your contribution is the implementation).

1. Make sure that you are in `master` branch by running `git status`. If not, run `git checkout master` to move to `master` branch.

1. Create a new branch on which you write your code. Use any branch name as you which. For example, `cool-feature`:

    ```bash
    git checkout -b cool-feature
    ```

1. Implement your contribution in the branch.

1. Periodically, and after you committed your changes, pull the latest changes from master. This ensures your branch is always up-to-date with the origin.

    ```bash
    git pull --rebase origin master
    ```

    Fix any conflicts that may arise.

1. After you really finished writing the code, commit your changes. You may create one or more commits.

1. Push the feature branch to `origin`:

    ```bash
    git push origin cool-feature
    ```

1. Create a new merge request on Gitlab for `cool-feature` branch to be merged to `master`. Refer the Pivotal Tracker's issue in the merge request description.

1. Wait for other project members and class instructors to review your contribution.

1. If they approve your contribution, congrats! Your contribution may be merged to master. First, don't forget to rebase your branch against master:

    ```bash
    git pull --rebase origin master
    ```

    Again, fix any conflicts that may arise.

1. Then, clean up your commits. Do a interactive rebase (please Google this term).

    ```bash
    git rebase -i origin/master
    ```

    You can pick, fix up, squash, or reorder the commits, or anything in any way you like. If necessary, rewrite the commit message to a more meaningful one.

1. Force-push your feature branch to origin:

    ```bash
    git push -f origin cool-feature
    ```

1. Ask the class instructors to merge your contribution to master.

1. After your contribution is merged, you may safely delete your feature branch:

    ```bash
    git branch -D cool-feature
    ```

    Also delete your feature branch on origin from Gitlab.

    ```bash
    git push origin :cool-feature
    ```

1. Done!
