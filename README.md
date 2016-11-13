# Pseudobook

## Start Guide

1. [Install Miniconda](http://conda.pydata.org/miniconda.html) (A Python package manager)

2. [Install homebrew](http://brew.sh/) (General purpose package manager for mac)

3. Install mysql
`brew install mysql`

4. Add mysql to PATH
`PATH=$PATH:/usr/local/mysql/bin`

5. Create pseudobook virtual environment
`conda env create -f environment.yml`

6. Activate pseudobook environment
`source activate pseudobook`

7. Navigate to pseudobook project dir
`cd pseudobook`

8. Set FLASK_APP environment variable
`export FLASK_APP=app.py`

9. Run App
`flask run`

## Dev Guide

1. Pull/Sync git repo master branch

2. Create new feature branch from master

3. Activate pseudobook environment
`source activate pseudobook`

4. Update environment packages if there are new dependencies
`conda env update -f environment.yml`

5. Navigate to pseudobook project dir
`cd pseudobook`

6. Set FLASK_APP environment variable
`export FLASK_APP=app.py`

7. Run App
`flask run`

8. Code out the feature on the new feature branch, test locally

9. When finished, pull/sync master branch again

10. Merge feature branch into master branch locally, resolve conflicts

11. Push/Sync master branch

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
