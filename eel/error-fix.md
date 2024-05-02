# Issue Summary:
When attempting to use the eel library in a Windows 11 environment with Python 3.12.0, I encountered an error where eel is unable to find the bottle.ext.websocket module, even though bottle-websocket is correctly installed in the Python environment. 

## Reproducible Example:

### Minimal example demonstrating the issue
```Python
import eel

eel.init("web")
eel.start("index.html")
```


## Expected Behavior:
I expected the script to run without errors and display the web application defined in index.html.
## Actual Behavior:
#### Encountered the following error:
```Python
Traceback (most recent call last):
 File "main.py", line 1, in <module>
 import eel
 File "C:\Users\Chetan\AppData\Local\Programs\Python\Python312\Lib\site-packages\eel\__init__.py", line 16, in <module>
 import bottle.ext.websocket as wbs
ModuleNotFoundError: No module named 'bottle.ext.websocket'
```

## Environment Details:
<pre>
Operating System: Windows 11
Python Version: 3.12.0
eel Version: 0.16.0
bottle Version: 0.12.25
bottle-websocket Version: 0.2.9
</pre>

## Steps to Reproduce:
Install eel, bottle, and bottle-websocket using pip.
Run the provided Python script in the specified environment.

## Additional Information:
I have tried a workaround by manually modifying the __init__.py file in the eel package to import bottle_websocket directly, which resolved the issue temporarily.

## Additional Testing:
##### I also tested the script on 
<pre>
Operating System: Windows 10
Python Version: 3.9.0
eel Version: 0.16.0
bottle Version: 0.12.25
bottle-websocket Version: 0.2.9
</pre>
##### In both cases, the following imports worked successfully:
```Python
import bottle_websocket as wbs
# or
import bottle.ext.websocket as wbs
```


