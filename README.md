# LOC-Auto-Transcriber
Flask webapp using Selenium, Pytesseract, and the OpenCV API that allows a user to login to their Library of Congress account to automatically transcribe from a collection of historical documents. User input implemented with PyWebIO.

## Instructions:

### To run this application, run this Docker command on your local CLI:

`docker run -p 4000:80 auto-transcriber`

### 1. Upon launching the file named `Autotranscriber.py`, you will be asked for four things in sequence from the application:

-Your Library of Congress By the People username and password

![image](https://user-images.githubusercontent.com/90420976/212444545-17365104-f0e1-49e4-8d97-55d6693d066a.png)

![image](https://user-images.githubusercontent.com/90420976/212444706-709ca694-22d6-4101-8c8a-ffe4a7a40b45.png)


-The amount of transcription cycles (total document transcriptions) you would like to perform while running this current instance.

![image](https://user-images.githubusercontent.com/90420976/212444750-99485fbb-9e9b-4c57-be17-ee7081081603.png)


-The time delay (in ms) for each automated Selenium task (will throw an error if below the minimum threshold of
500ms to prevent arousing suspicion of bot activity).

![image](https://user-images.githubusercontent.com/90420976/212445132-d78a3654-a25f-4532-a5e0-ffa6553c7e16.png)


### 2. When the Auto-Transcriber has picked a random archive for you, you must manually pick which document must be transcribed. 

**The Auto-Transcriber is set to be dormant until you pick a document to transcribe. There is a 500 second timeout toggle; if the user has been idle for 500 seconds or longer, the application will automatically time out and exit.**

Upon reaching a historical document with its transcription field, the Auto-Transcriber will automatically go into fullscreen mode, and begin to transcribe documents. This sequence will repeat until the amount of requested transcription cycles has been reached.

 All transcription sequences are logged into an AWS DynamoDB database with a unique UUID assigned to each successful transcription.





