# pysignal

Functions and tests for signal processing
By Roeland Huys.  Find me on GitLab: https://gitlab.com/rhuys/pysignal.git


# INSTALLATION for development and testing

Extract from Gitlab:

`git clone https://github.com/rhuys/pysignal.git`

To use the library in Python, you may have to add the folder to the python path:

**in Windows**
`set PYTHONPATH=%PYTHONPATH%;%USERPROFILE%\python\pysignal`

You can also edit in the dialog Settings -> Edit environment variables for your account, or run:
`rundll32 sysdm.cpl,EditEnvironmentVariables`

To test: `echo %PYTHONPATH%`


## HOW TO MAKE A VIRTUAL ENVIRONMENT FOR TESTING

In case installation of Python packages is blocked by your Admin, use a virtual environment:

1. Open a terminal and cd to the main project folder.  In Windows, you need to use Windows Command prompt (it does not work in Powershell) 
2. ``python -m venv venv``
3. To activate the venv from the command shell: ``venv\Scripts\activate``
4. To activate the venv from VSCODE: go to the Python plugin and select the environment
5. Make sure in VSCODE, you do Ctrl+Shift+P, ``Python: Select Interpreter``, choose the one from ``venv``

## PACKAGES

`pip install numpy matplotlib scipy`

## IPYTHON

To make ipython run better, edit the default profile.
First find the profile folder:
`ipython profile locate`

In this folder, create a folder 
In that file, add following lines:

```
# profile_default for ipython 
# .ipython/profile_default/startup/00-startup.ipy

# make matplotlib interactive and smooth
%matplotlib   

# make sure ipython always reloads modules
%load_ext autoreload
%autoreload 2

import numpy as np
import matplotlib.pyplot as plt

plt.ion()
```

# VERSIONS

