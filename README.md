# LOC-Auto-Transcriber
PywebIO webapp that allows a user to login to their Library of Congress account to automatically transcribe from a collection of historical documents.

## Instructions:

**Note: You will need to have Selenium for Python installed on your desktop for this program to work.**

### 1. Upon launching the file named `Autotranscriber.py`, you will be asked for four things in sequence from the application:

-Your Library of Congress By the People username and password
-The amount of transcription cycles (total document transcriptions) you would like to perform while running this current instance.
-The time delay (in ms) for each automated Selenium task (will throw an error if below the minimum threshold of
500ms to prevent arousing suspicion of bot activity).

### 2. When the Auto-Transcriber has picked a random archive for you, you must manually pick which document must be transcribed. 

-Upon reaching  with its transcription field, the Auto-Transcriber will automatically go into fullscreen mode,   This sequence will repeat until the amount of requested transcription cycles has been reached.




