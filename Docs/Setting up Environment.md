<h1>  Setting Up Environment </h1>

This will guide you how to setup virtual environment for yolov5 v4.


You can install pip yourself to ensure you have the latest version.

```
python3 -m pip install --user --upgrade pip
```

<h3> Create a virtual environment </h3>

To create a virtual environment, go to your project’s directory and run venv. If you are using Python 2, replace venv with virtualenv in the below commands.

```
py -m venv env
```

<h3> Activating a virtual environment </h3>

Before you can start installing or using packages in your virtual environment you’ll need to activate it.

```
.\env\Scripts\activate
```


<h3> Installing Required Modules for Yolov5 v4 </h3>
This will guide you how to install all the required modules especially for yolov5 version 4.
 
Go to Yolov5-4.0 github repo and download the repository in zip formant. After that, Extract the zip in your working directory
```
https://github.com/ultralytics/yolov5/tree/v4.0
```

Move to your yolov5 directory.
  
```
cd yolov5-4.0
```

install the required modules for yolov5 v4. This will install all the required modules.

```
pip install -r requirements.txt
```


<h3> Leaving the virtual environment </h3>

If you are done with your project you can leave your virtual environment, simply run:

```
deactivate
```
