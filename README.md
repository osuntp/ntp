<p align="center">
  <a href="" rel="noopener">
 <img height=200px src="media/logo.png?raw=true" alt="Project logo"></a>
</p>

<h1 align="center">NTP (NET) Software</h3>

<p align="center">This repository contains the software developed for the Nonnuclear Environmental Testing (NET) Facility, located at The Ohio State University.
    <br> 
</p>

## Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Authors](#authors)

## About <a name = "about"></a>
Within this repository are the codes, configuration files, data processing workflows, and documentation related to conducting experiments using the NTP NET Facility, located in W092, Scott Lab.

## Directory
At a high level, the repository is broken down into several subdirectories. The big ones are:
- `App`: main directory for code relating to the test facility software
- `Arduino`: firmware for the data acquisition system and the insturmentation control system
- `Post`: code used to post-process test data

And there are additional subdirectories for logs, configuration files, documentation, a sandbox, etc.

## Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites
The software was built using [Anaconda](https://www.anaconda.com/) and [VS Code](https://code.visualstudio.com/) in [Python 3.8](https://www.python.org/downloads/release/python-380/). To use the software, it is recommended to create a Conda Environment and use the `requirements.txt` file located in the main directory of this repository.

### Installing
Begin by downloading or otherwise cloning the repository to your desired directory. You may simply download a [compressed (.zip) archive](https://github.com/gulanr/ntp/archive/refs/heads/main.zip) of everything, or use [Git](https://git-scm.com/), [GitHub Desktop](https://desktop.github.com/), or even VS Code's source control management tools to keep an up-to-date copy of the code.

In Conda, ensure your desired environment is active, and open the `CMD.exe Prompt` application. You'll know things are set up properly if the command prompt displays something like:

```
(ntp) C:\Users\noahr>
```

where "`ntp`" is the name of the environment you created in Conda. Next, navigate to wherever you downloaded the source code to (using the `cd` command, for example), and enter
```
> pip3 install -r requirements.txt
```

This will automatically install the Python modules and packages necessary to run the source code. Once this is complete, you can enter
```
> python App\main.py
```
to launch the software and verify that everything was installed correctly.

## Usage <a name="usage"></a>
Complete documentation on the usage and its instructions are still being created. In the meantime, running the `main.py` Python file in the `App` directory will start the software.

### Development
There is no formal development methodology in this project. The authors of the software are aerospace engineers, not software engineers, and therefore, features and fixes have been implemented on an "as needed" basis in response to issues discovered in lab or while using the software. There is no product road map extending beyond what can be achieved in the next couple of weeks.

If you are a researcher using the software and would like to recommend a new feature that would be convenient to your work, you are encouraged to reach out to the "custodians" of the software, listed below.

If you are adept in software development and have interest in the project, there are probably a billion things which can be cleaned up, improved, or completely overhauled and redone. Get in touch if you want to chip in.

## Authors <a name = "authors"></a>
- [@gulanr](https://github.com/gulanr)
- [@jakestonehill](https://github.com/jakestonehill)

See also the list of [contributors](https://github.com/gulanr/ntp/contributors) who participated in this project.