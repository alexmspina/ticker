# Ticker Development Environment

<br/>

## Version Control

---

### Getting Set Up for Local Development

`git clone `

<br/>

### Git Flow

Ticker uses the [Git Flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) pattern to manage feature, hotfix, and release development branches.

<br/>

#### Branches

`main` is the primary branch from which tagged releases will be created. Ticker uses `main` instead of `master` to align with GitHub's decision to switch the default naming convention from `master` to `main`

`develop` is the branch on which most development will be done.

`feature` branches will stem from `develop` and merged back into `develop` on completion. Feature branches are prefixed with `feature/` annotation.

`hotfix` branches stem from `main` and are merged back into `main` and into `develop` upon completion. Hotfix branches are prefixed with `hotfix/`.

`release` branches stem from `develop` and are merged back into `develop` and into `main` upon completion. Release branches are prefixed with `release`.

`bugfix` branches are similar to `hotfix` branches, but shoul dbe stemmed from `release` branches.

`support` branches are very similar to `hotfixes`, but they should be treated as less severe as hotfixes and therefore are allowed more time to complete. They are also stemmed from `main`

<br/>

#### CLI Implementations

There are several cli implementations for Git Flow. [gitflow-avh](https://github.com/petervanderdoes/gitflow-avh) is a popular flavor that extends the `git` cli and handles many of the operations the Git Flow pattern utilizes. It also expands upon the original `git-flow` cli.

<br/>

#### Feature Development

Features are added by branching off `develop`. These are always merged back into `develop` and they are never merged directly into `main`, `release`, or `hotfix` branches.

##### Initializing a Repo with Git Flow

`git flow init`

This will start a prompt where you can name the default names for project branches. Use the branch names listed above.

##### Starting a New Feature

`git flow feature start [feature-name]`

This will create a new branch from the `develop` branch named `feature/feature-name`

<br/>

##### Publishing a Feature for Collaboration

`git flow feature publish [feature-name]`

This will push the the `feature/feature-name` branch to the remote repository so others can pull it down for collaboration.

<br/>

##### Finishing a Feature

`git flow feature finish [feature-name]`

This will merge the feature branch back into `develop`. For now features can be merged directly into develop, but it might make sense to implement a pull request review step once the team grows.

<br/>

#### Release Development

Releases are added by branching off `develop`. These act as planning stages before merging into `main` where it will be tagged and released. Only bug development, clean-up, and final touches will be performed on these branches.

<br/>

##### Starting a New Release

`git flow release start [release-name]`

This will create a new branch from the `develop` branch named `release/release-name`

<br/>

##### Publishing a Release for Collaboration

`git flow release publish [release-name]`

This will push the the `release/release-name` branch to the remote repository so others can pull it down for collaboration.

<br/>

##### Finishing a Release

`git flow release finish [release-name]`

This will merge the release branch into `main` and back into `develop`, however this should be done in a pull request review on GitHub for added safety.

<br/>

#### Additional Branches

`gitflow-avh` supports other branches including bugfixes, hotfixes, and support tickets. They can be created, finished, and deleted using the same cli syntax as other branches. 

<br/>

##### Bugfix Branches

Bugfix branches should be stemmed from release branches.

<br/>

##### Hotfix Branches

Hotfix branches should be stemmed from `main`.

<br/>


##### Support Branches

Support branches should be stemmed from `main`.

<br/>
<br/>

## Development Environment

---

### Python Versioning

Ticker uses pyenv to set the local version of Python. The local Python version can be found in the .python-version file. `pyenv` can be installed it using `brew install pyenv` on a Mac or `choco install pyenv-win` on a Windows PC.

<br/>

### Dependency Management

Ticker uses `poetry` to manage its dependencies, virtual environments, and packaging. It uses a `pyproject.toml` file for building and packaging projects. `pyproject.toml` can be thought of as a modern approach to a `setup.py` file. Dependency versions are defined in the `poetry.lock` file and provide a mechanism for reporducible builds. It can be installed using `pip install poetry`. 

<br/>

#### Starting a Virtual Environment

The first time you start a virtual environment, use `poetry install` to ensure all the dependencies and the virtual environment is set up correctly. Poetry will keeps track of virtual environments and you can view available environments on your machine using `poetry env list`.


After that you can use `poetry shell` to start the virtual environment.


<br/>

#### Package Installation

`poetry add [package]`

Use the `--dev` or `-D` flag when install packages related to things like formatting, linting, testing, etc.

`poetry add --dev [package]`

<br/>

#### Package Removal

`poetry remove [package]`

Use the `--dev` or `-D` flag when uninstall development packages.

`poetry remove --dev [package]`

<br/>

### Linting

Ticker uses `pylint` and the VS Code Python and Pylance extensions for linting and type checking. You may need to change the path to your `poetry` binary and virtual environment in the `.vscode/settings.json` file.

<br/>

### Formatting

Ticker uses `black` to format all `.py` files.

<br/>

### Testing

Ticker uses a mixture of `unittest` and `pytest` based unit tests. Originally, tests were added using the standard library's `unittest` package and TestCase class pattern. `pytest` based tests were added later to take advantage of the `pytest.fixutres` feature and its database mocking abilities. `unittest` based tests will probably be refactored to the `pytest` pattern, but `unittest` based tests can be executed using `pytest`.

<br/>

#### Test Structure

Test files are located in the same folder as the source code they test. This differs from the pythonic test structure which places the `tests` directory in the root of the project.

#### Running Tests

To run all the unit tests use the command `pytest **/*_test.py`.

<br/>

#### Test Coverage Reports

Test coverage reports can be run using the command `pytest --cov=. **/*_test.py`

<br/>

#### Display Test Results By Function

`pytest --verbose --cov=. **/*_test.py`

<br/>
<br/>

## SQL Database Operations

---

Ticker uses a PostgreSQL database for persistent storage and leverages the `psycopg2` adapter to interact with the service. 

<br/>

### psycopg2 Documentation

https://www.psycopg.org/docs/index.html

<br/>

### psycopg2 installation

Pyscopg requires the `pg_config` executable. Install it using the following commands, according to your operating system.

<br/>

#### MacOS
`brew install postgresql`

<br/>

#### Windows
`choco install postgresql`

<br/>

#### Linux
```
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql
```

<br/>

#### Use pip to install psycopg2-binary

`poetry add pyscopg2-binary`.

<br/>

##### pyscopg2 vs psycopg2-binary
`psycopg2-binary` includes C libraries so you don't have to build from source.

<br/>

#### Troubleshooting
##### MacOS openssl installation issues 
If you see an error including the text `ld: library not found for -lssl` try setting the `LDFLAGS` environment variable to your location of openssl. For homebrew users it will look similar to `export LDFLAGS="-L/opt/homebrew/opt/openssl/lib"`

<br/>

### SQL Statements

SQL functions and statements are maintained with the `aiosql` package. `aiosql` uses a lowercase SQL syntax which allows SQL statements to be codified and accessed like traditional Python functions and methods.

<br/>

#### aiosql Documentation

https://nackjicholson.github.io/aiosql/

<br/>

## Enabling HTTPS

In order to enable HTTPS for the Ticker service, the paths to the SSL certificate and SSL key files need to be provided using the `TICKER_SSL_CERTIFICATE` and `TICKER_SSL_KEY` environment variables or the `--sslcert` and `sslkey` command line options.

#### Configuring HTTPS for Local Development

Although not necessary, configuring HTTPS can be helpful for some local development workflows. To configure your environment for local HTTPS development you can follow these steps:

1. Download the [Minica certificate authority tool](https://github.com/jsha/minica)
2. Generate certificates and keys using `minica` for a domain of your choosing; For security reasons choose a domain you know doesn't exist like `ticker.example.something`
3. Add an alias to your hosts file for the Ticker server host you set by environment variable or command line option that resolves to the domain for which you generated certificates
4. Add the `minica.pem` you generated in step 2 to you local certificate trust store; rename it to something that references the project and is memorable so you can delete it when it is no longer needed
5. Pass the `<domain chosen in step 2>/cert.pem` and `<domain chosen in step 2>/key.pem` files generated in step 2 to the Ticker server using the environment variables or command line options mentioned in the Enabling HTTPS section.
6. Make requests against the domain you chose in step 2; your browser should be able to resolve the host because of alias you added to your local hosts file 