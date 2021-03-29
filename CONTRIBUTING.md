# How to contribute

First things first, thank you for taking the time to read this because every little bit of help is appreciated. 😁

This is project is really simple (and not inovative at all 😅) and is being developed for fun on my free time only, as of consequence is not intented to be complex or extensive.

All the usage is on the [README](https://github.com/JBizarri/steganography/blob/master/README.md) file.

## Development

>We currently develop only in Python 3.8.X

First you should clone or fork the repository. Then create and activate a virtualenv to install all dependencies by running the following command inside the newly created steganography folder:

`$ python3 -m virtualenv venv && source venv/bin/activate`

Install the dependecies with `poetry install` ([Poetry documentation](https://python-poetry.org/docs/)) and don't forget to install the pre-commit hooks by running `poetry run pre-commit install`.
We use `tox` together with `pre-commit` to automate checks for linting, formatting, testing and generating documentation.

We use PyTest as our testing framework. All tests are inside the `tests` folder and we use the same structure as the main code for easily finding where the tested file is. For instance the test file for `steganography/steganography.py` code is inside `tests/steganography/test_steganography.py`.

We use Flake8 for linting and Black for formatting code.

We use pdoc3 for generating our documentation with a custom template inside `docs/templates/text.mako`.

> For a more detailed view of the CI check out the [tox.ini](tox.ini) file

## Submitting changes

Please send a [GitHub Pull Request to Steganography](https://github.com/JBizarri/steganography/compare) with a clear list of what you've done and update any documentation that is relevant (read more about [pull requests](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests)). When you send a pull request, we will love you forever if you include tests for new features. We can always use more test coverage. Please follow our coding conventions (below) and make sure all of your commits are atomic (one feature per commit).

Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

    $ git commit -m "A brief summary of the commit
    > 
    > A paragraph describing what changed and its impact."

>If you're not sure how you should be writing your commit messages, check out [this amazing article](https://chris.beams.io/posts/git-commit/) by Chris Beams.

## Coding conventions

Start reading our code and you'll get the hang of it. We optimize for readability:

  * We indent using four spaces
  * We follow PEP8 naming convetion
  * We use Black (default settings) to format our code
  * We use Flake8 for linting, excluding a few rules, such as "E203" and "W503". Any future exclusions will be added to the [tox.ini](tox.ini) file.
  * This is open source software. Consider the people who will read your code, and make it look nice for them.

And again, thank your being interested in Steganography. ❤

## References

Adapted from The Open Government [contribution guidelines.](https://github.com/opengovernment/opengovernment/blob/master/CONTRIBUTING.md)
