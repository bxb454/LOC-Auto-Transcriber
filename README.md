# LOC-Auto-Transcriber
PywebIO webapp using Selenium, Pytesseract, and OpenCV libraries that allows a user to login to their Library of Congress account to automatically transcribe from a collection of historical documents.

## Instructions:

**Note: You will need to have Selenium for Python installed on your desktop for this program to work.**

### 1. Upon launching the file named `Autotranscriber.py`, you will be asked for four things in sequence from the application:

-Your Library of Congress By the People username and password

![image](https://user-images.githubusercontent.com/90420976/212444545-17365104-f0e1-49e4-8d97-55d6693d066a.png)

![image](https://user-images.githubusercontent.com/90420976/212444706-709ca694-22d6-4101-8c8a-ffe4a7a40b45.png)


-The amount of transcription cycles (total document transcriptions) you would like to perform while running this current instance.

-The time delay (in ms) for each automated Selenium task (will throw an error if below the minimum threshold of
500ms to prevent arousing suspicion of bot activity).

### 2. When the Auto-Transcriber has picked a random archive for you, you must manually pick which document must be transcribed. 

-Upon reaching  with its transcription field, the Auto-Transcriber will automatically go into fullscreen mode,   This sequence will repeat until the amount of requested transcription cycles has been reached.




