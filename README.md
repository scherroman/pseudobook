# Pseudobook

Built with [Edgar Samudio](https://github.com/esamudio) and [Alex Scarlatos](https://www.linkedin.com/in/alex-scarlatos-399455113/)

## Start Guide

**1 - [Install Miniconda 3.5](http://conda.pydata.org/miniconda.html) (A Python package manager)**

**2 - [Install Homebrew](http://brew.sh/) (General purpose package manager for mac)**

**3 - Add homebrew to top of path by adding the text below to bottom of `~/.bash_profile`**

```
#Homebrew
export PATH=/usr/local/bin:/usr/local/sbin:$PATH
```

**4 - Install mysql via homebrew**

`brew install mysql`

**5 - Run mysql setup scripts**

Login as root

`mysql -u root -p`

Setup tables, Create pseudobook user

`source Pseudobook.sql`

Add user transaction procedures

`source UserTransactions.sql`

Add manager and sales oriented transaction procedures

`source ManagerEmployeeCustomerTransactions.sql`

**6 - Create pseudobook virtual environment**

`conda env create -f environment.yml`

**7 - Activate pseudobook environment**

`source activate pseudobook`

**8 - Set Flask environment variables**

`export FLASK_APP=app.py && export FLASK_DEBUG=1`

**9 - Run App**

`cd pseudobook`

`flask run`

## Dev Guide

**1 - Pull/Sync git repo master branch**

**2 - Create new feature branch from master**

**3 - Activate pseudobook environment**

`source activate pseudobook`

**4 - Update environment packages if there are new dependencies**

`conda env update -f environment.yml`

**5 - Wipe/Recreate database if there are changes to sql tables (rather than dealing with migrations)**

Login as root

`mysql -u root -p`

Setup tables

`source Pseudobook.sql`

Add user transaction procedures

`source UserTransactions.sql`

Add manager and sales oriented transaction procedures

`source ManagerEmployeeCustomerTransactions.sql`

**6 - Set Flask environment variables**

`export FLASK_APP=app.py && export FLASK_DEBUG=1`

**7 - Run App**

`cd pseudobook`

`flask run`

**7 - Code out the feature on the new feature branch, test locally**

**8 - When finished, pull/sync master branch again**

**9 - Merge feature branch into master branch locally, resolve conflicts**

**10 - Push/Sync master branch**

## Helpful stuff

List environments

`conda info --envs`

Activate an environemnt

`source activate pseudobook`

Deactivate an environemnt

`source deactivate pseudobook`

Delete an environment

`conda remove --name pseudobook --all`

List environment packages

`conda list`

Install a package

`pip install package_name`

Delete a package

`pip uninstall package_name`
