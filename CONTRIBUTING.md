# Contributing to FastEdit

First and foremost, thank you for considering contributing to FastEdit! Your contributions are essential to the success of this project, and we're thrilled to have you as part of our community.

We believe that collaboration is key to driving innovation and ensuring the highest quality of code and features. By following the guidelines in this document, you will help us maintain the project's quality, streamline the review process, and make it easier for everyone to contribute.

This document outlines the ways you can get involved and the steps to ensure your contributions are successfully integrated. Whether you're fixing a bug, adding a new feature, or improving our documentation, your input is invaluable and greatly appreciated.

## Table of contents

[1. Create an issue](#1-create-an-issue)
[2. Fork the repository and create a branch](#2-fork-the-repository-and-create-a-branch)
[3. Set up your development environment](#3-set-up-your-development-environment)
[4. Make your changes](#4-make-your-changes)
[5. Add or update documentation](#5-add-or-update-documentation)
[6. Add or update tests](#6-add-or-update-tests)
[7. Submit a pull request](#7-submit-a-pull-request)
[8. Code review and feedback](#8-code-review-and-feedback)

## 1. Create an issue

Before you start working on a contribution, please create an Issue in our GitHub repository. This helps us track your idea, discuss it, and check if it’s already being addressed or planned. When creating an issue, please provide as much detail as possible to clearly describe the problem or enhancement.

If you are interested in working on the issue, feel free to mention this by adding the label "want to contribute". This helps us coordinate efforts and avoid duplicate work.

## 2. Fork the repository and create a branch

Once the issue has been discussed and approved for work, you can start by [forking the repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo). After forking, create a new branch from the main branch. We recommend naming your branch descriptively, with the modification type as a prefix (feature, fix, or docs), such as:
- feature/your-feature-name
- fix/your-fix-name
- docs/your-docs-name

## 3. Set up your development environment

After you've created your branch, set up your development environment according to the project's setup instructions. This typically involves installing dependencies and configuring the environment to ensure everything runs smoothly.

## 4. Make your changes

Now you’re ready to start coding! Please make sure that your code adheres to our coding standards and style guidelines. For Python code, ensure that your code follows PEP 8 and that your docstrings are in the Numpydoc format.

## 5. Add or update documentation

If your changes affect the public API, features, or functionality, please update the relevant documentation. Keeping our documentation up to date is crucial for users and other contributors to understand how the project works. This might involve updating docstrings, README files, or any other relevant documentation files.

## 6. Add or update tests

Testing is vital to maintaining the quality of our project. If your changes include new features, bug fixes, or refactoring, please add or update unit tests, integration tests, or other relevant tests in the tests directory. Each type of test has its corresponding subfolder (e.g., unit, integration).

Before submitting your changes, make sure all tests pass locally:

```bash
pytest
```

## 7. Submit a pull request

Once you’ve completed your changes, you’re ready to submit a Pull Request (PR). Push your branch to your forked repository:

```bash
git push origin feature/your-feature-name
```
Then, open a Pull Request to the original repository. When naming your Pull Request, please follow the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/). This helps us maintain a clear and consistent commit history.

In your PR description, please reference the issue you are addressing (e.g., "Closes #123") and describe the changes you've made in detail. Make sure to fill out any PR templates provided and follow any checklist items.

## 8. Code review and feedback

Our maintainers will review your PR, and we might ask for some modifications or clarifications before merging the code. Don’t worry if this happens—it’s a normal part of the process, and our goal is to collaborate to get the best result.. Once everything looks good, your contribution will be merged into the project!