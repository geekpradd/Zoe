##Zoe: FTP extensions for git 

Zoe is a Python based command line utility that helps in using FTP clients with git. Zoe uses git commands to push, pull and sync your git repo contents with a Remote FTP server. 

Zoe is under development and once completed, Zoe will use the PyFTP module and will be available for installation on PyPI.

###Usage 

Firstly navigate to your git repo and enter

```
zoe
```
You will need to enter your FTP details. 

To push changes,

```
zoe push
```

If this is your first push, then your entire repo will be copied over.
If not, then Zoe will only sync changed files in the latest commit.

In order to sync or push files, you need to make a new commit. Otherwise Zoe will not comply and will leave a warning. 

To pull changes from FTP server,

```
zoe pull
```

This function is currently incomplete (under development) as it has some errors with folder handling 

To list files,

For local repo:

```
zoe list
```

For FTP server

```
zoe list server
```

To change FTP host name, password, username etc 

```
zoe modify
```

Incase you need to forcefully push all files (like what happened when you made your first push), use 

```
zoe push --force
```

This is useful, incase you rollbacked to a previous commit in git.

###To-Do

1. Complete the `zoe pull` function 
2. Create setup.py, package the python files and upload to PyPI and Chocolatey 
3. Add support for untracked files (files that are not in git but should be pushed to FTP server)
4. Add support for multiple FTP servers (like git origins)

###About

Created by Pradipta. Copyright 2015. MIT Licensed