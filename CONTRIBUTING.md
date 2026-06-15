# Contributing to ShieldEye

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them. Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. The community looks forward to your contributions. 🎉

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
>
> - Star the project
> - Tweet about it
> - Refer this project in your project's readme
> - Mention the project at local meetups and tell your friends/colleagues

## Table of Contents

- [Contributing to ShieldEye](#contributing-to-shieldeye)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct](#code-of-conduct)
  - [I Have a Question](#i-have-a-question)
  - [I Want To Contribute](#i-want-to-contribute)
    - [Reporting Bugs](#reporting-bugs)
      - [Before Submitting a Bug Report](#before-submitting-a-bug-report)
      - [How Do I Submit a Good Bug Report?](#how-do-i-submit-a-good-bug-report)
    - [Suggesting Enhancements](#suggesting-enhancements)
      - [Before Submitting an Enhancement](#before-submitting-an-enhancement)
      - [How Do I Submit a Good Enhancement Suggestion?](#how-do-i-submit-a-good-enhancement-suggestion)
    - [Your First Code Contribution](#your-first-code-contribution)
      - [Prerequisites](#prerequisites)
      - [Setting Up the Development Environment](#setting-up-the-development-environment)
      - [Making Your Changes](#making-your-changes)
      - [Build Requirements (Optional)](#build-requirements-optional)
    - [Improving The Documentation](#improving-the-documentation)
      - [How to Contribute to Documentation](#how-to-contribute-to-documentation)
      - [Guidelines](#guidelines)
  - [Styleguides](#styleguides)
    - [Commit Messages](#commit-messages)
      - [Format](#format)
      - [Types](#types)
      - [Examples](#examples)
      - [Rules](#rules)
  - [Join The Project Team](#join-the-project-team)
  - [Attribution](#attribution)

## Code of Conduct

This project and everyone participating in it is governed by the
[ShieldEye Code of Conduct](./CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior
to [report@holoolagoke.com](mailto:report@holoolagoke.com).

## I Have a Question

> If you want to ask a question, we assume that you have read the available [Documentation](https://holoolagoke.github.io/shield-eye-desktop).

Before you ask a question, it is best to search for existing [Issues](https://github.com/holoolagoke/shield-eye-desktop/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/holoolagoke/shield-eye-desktop/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (nodejs, npm, etc), depending on what seems relevant.

We will then take care of the issue as soon as possible.

## I Want To Contribute

### Legal Notice
>
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project licence.

### Reporting Bugs

#### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions (Make sure that you have read the [documentation](https://holoolagoke.github.io/shield-eye-desktop). If you are looking for support, you might want to check [this section](#i-have-a-question)).
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/holoolagoke/shield-eye-desktop/issues?q=label%3Abug).
- Also make sure to search the internet (including Stack Overflow) to see if users outside of the GitHub community have discussed the issue.
- Collect information about the bug:
- Stack trace (Traceback)
- OS, Platform and Version (Windows, Linux, macOS, x86, ARM)
- Version of the interpreter, compiler, SDK, runtime environment, package manager, depending on what seems relevant.
- Possibly your input and the output
- Can you reliably reproduce the issue? And can you also reproduce it with older versions?

#### How Do I Submit a Good Bug Report?

> You must never report security related issues, vulnerabilities or bugs including sensitive information to the issue tracker, or elsewhere in public. Instead sensitive bugs must be sent by email to [report@holoolagoke.com](mailto:report@holoolagoke.com).

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/holoolagoke/shield-eye-desktop/issues/new). (Since we can't be sure at this point whether it is a bug or not, we ask you not to talk about a bug yet and not to label the issue.)
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the *reproduction steps* that someone else can follow to recreate the issue on their own. This usually includes your code. For good bug reports you should isolate the problem and create a reduced test case.
- Provide the information you collected in the previous section.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps and mark the issue as `needs-repro`. Bugs with the `needs-repro` tag will not be addressed until they are reproduced.
- If the team is able to reproduce the issue, it will be marked `needs-fix`, as well as possibly other tags (such as `critical`), and the issue will be left to be [implemented by someone](#your-first-code-contribution).

[bug report template](./.github/ISSUE_TEMPLATE/bug_report.yaml)

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for ShieldEye, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Read the [documentation](https://holoolagoke.github.io/shield-eye-desktop) carefully and find out if the functionality is already covered, maybe by an individual configuration.
- Perform a [search](https://github.com/holoolagoke/shield-eye-desktop/issues) to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset. If you're just targeting a minority of users, consider writing an add-on/plugin library.

#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/holoolagoke/shield-eye-desktop/issues).

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.
- You may want to **include screenshots or screen recordings** which help you demonstrate the steps or point out the part which the suggestion is related to. You can use [LICEcap](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and the built-in [screen recorder in GNOME](https://help.gnome.org/users/gnome-help/stable/screen-shot-record.html.en) or [SimpleScreenRecorder](https://github.com/MaartenBaert/ssr) on Linux.
- **Explain why this enhancement would be useful** to most ShieldEye users. You may also want to point out the other projects that solved it better and which could serve as inspiration.

### Your First Code Contribution

#### Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.8 or higher** — [Download](https://www.python.org/downloads/)
- **Git** — [Download](https://git-scm.com/)
- **SQLCipher** (Linux only) — required by `sqlcipher3`

```bash
  sudo apt install libsqlcipher-dev
```

#### Setting Up the Development Environment

  1. Fork and clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/shield-eye-desktop.git
cd shield-eye-desktop
```

Create a virtual environment

```bash
python -m venv venv

# Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Install runtime dependencies

```bash
pip install -r requirements.txt
```

Create your `.env` file in the project root. Copy the structure below and fill in your values:

```env
APP_NAME=ShieldEye
APP_VERSION=1.1.0
DB_NAME=database.db
APPNAME=my_app_name
THEUSER=the_app_user
GITHUB_UPDATE_URL=https://raw.githubusercontent.com/holoolagoke/shield-eye-desktop/main/version.json
GITHUB_URL=https://github.com/holoolagoke/shield-eye-desktop
WEBSITE_URL=https://www.holoolagoke.com
SHIELDEYE_WEBSITE_URL=https://shieldeye.holoolagoke.com
DEVELOPER_NAME=Holo Olagoke
DEVELOPER_CONTACT=contact@holoolagoke.com
DEV_MODE=production
```

Run the app from source

```bash
python main.py
```

#### Making Your Changes

- Create a new branch for your work:

```bash
  git checkout -b feature/your-feature-name
  # or
  git checkout -b fix/your-bug-fix-name
```

- Make your changes, following the existing code style.
- Test your changes manually by running the app and exercising the affected functionality.
- Commit your changes following the [commit message guidelines](#commit-messages).
- Push your branch and open a Pull Request against the `master` branch with a clear description of what you changed and why.

#### Build Requirements (Optional)

If you want to compile the app into a binary, install the build dependencies separately:

```bash
pip install -r build_requirements.txt
```

> Do **not** install `build_requirements.txt` for normal development — it is only needed to produce the `.deb` or `.exe` release artifacts.

### Improving The Documentation

Documentation lives in the following places — contributions to any of them are welcome:

| File                            | Purpose                                                   |
|---------------------------------|-----------------------------------------------------------|
| `README.md`                     | Main project overview, quick start, and integration guide |
| `How_to_integrate_ShieldEye.md` | Full instrumentation and logger setup tutorial            |
| `DESKTOP_INSTALLATION.md`       | Linux and Windows installation instructions               |
| `CHANGELOG.md`                  | Release history                                           |

#### How to Contribute to Documentation

- **Fix a typo or unclear wording** — open a Pull Request directly with your edit.
- **Add a missing example** — if you integrated ShieldEye into a framework or language not yet covered (e.g. Django, FastAPI, Spring Boot), a code example addition to `How_to_integrate_ShieldEye.md` is very welcome.
- **Report a documentation issue** — open a [GitHub Issue](https://github.com/holoolagoke/shield-eye-desktop/issues/new) with the label `documentation`, describe what is wrong or missing, and where.

#### Guidelines

- Write in clear, plain English. Assume the reader is a developer but not necessarily a security expert.
- Keep code examples minimal and self-contained.
- If you add a new section to `README.md`, add a corresponding entry to the Table of Contents.
- All documentation is written in Markdown. Preview your changes locally before submitting.

## Styleguides

### Commit Messages

ShieldEye uses a simplified version of the [Conventional Commits](https://www.conventionalcommits.org/) standard.

#### Format

- **type** — what kind of change this is (see table below)
- **scope** — the part of the codebase affected, in lowercase (optional but encouraged)
- **short summary** — present tense, lowercase, no period at the end

#### Types

| Type       | When to use                                |
|------------|--------------------------------------------|
| `feat`     | A new feature                              |
| `fix`      | A bug fix                                  |
| `docs`     | Documentation changes only                 |
| `style`    | Formatting, whitespace — no logic change   |
| `refactor` | Code restructure with no feature or fix    |
| `perf`     | Performance improvement                    |
| `chore`    | Build process, dependency updates, tooling |
| `security` | Security-related fix or hardening          |

#### Examples

\```  
feat(dashboard): add keyword search to log table  
fix(updater): fallback to xterm when gnome-terminal not found  
docs(readme): correct Linux installation download URL  
security(db): enforce minimum PRAGMA key length at creation  
chore(deps): bump PySide6 to 6.11.0  
refactor(preferences): access prefs row by column name instead of index  
\```

#### Rules

- Keep the summary under 72 characters.
- Use the body (separated by a blank line) to explain *why*, not *what*, for non-obvious changes.
- Reference related issues at the bottom of the body: `Closes #42` or `Ref #17`.
- Do not commit commented-out code, debug `print()` statements, or `.env` files.

## Join The Project Team

ShieldEye is currently maintained by [Holo Olagoke](https://www.holoolagoke.com) as an open-source project.

If you have made several meaningful contributions — bug fixes, features, or documentation — and are interested in becoming a regular collaborator with triage or review access, reach out directly:

- **Email:** [contact@holoolagoke.com](mailto:contact@holoolagoke.com)
- **GitHub:** [@holoolagoke](https://github.com/holoolagoke)

Include a brief note about your background, what contributions you have made or plan to make, and what area of the project you are most interested in (UI, detection logic, documentation, packaging, etc.).

There is no formal process yet — it is a conversation. All contributors are credited in release notes and the project's acknowledgements.

## Attribution

This guide is based on the [contributing.md](https://contributing.md/generator)!
