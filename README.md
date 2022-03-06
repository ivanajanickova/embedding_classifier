# Demo - Projects Overview

Overview of all the (public) projects implemented by Radix, presented as a demo.



## Setup Project

In order to install the project environment locally, run `./tasks/init.sh` from Terminal in the project's root folder. 
When successful, you can activate the project's environment by running `source activate yield-validation-env`.

A list of project-tasks exist, which can be summon using the `invoke` command:
- `invoke bump` Bump the major, minor, patch, or post-release part of this package's version.
- `invoke docs` Generate this package's docs.
- `invoke lab` Run Jupyter Lab.
- `invoke lint` Lint this package. 
- `invoke test` `Test this package.
- `invoke conda.create` Recreate the conda environment.
- `invoke conda.update` Update the conda environment.
- `invoke --list` Get overview of all the `invoke` commands.

It is possible to extend the `invoke` list by adding your own task in the `./tasks/tasks.py` file.



## Installation

To install this package in your environment, run:

```bash
pip install git+ssh://git@gitlab.com/radix-ai/internal/demo-projects-overview.git@v0.0.0
```

