# pngk
# Requirments

During the call
Part 1 - .mp3_Audio http://roelofvandijk.com/mp33/IVR/PNGK-whereAreYouFrom.mp3 
If the caller does say something the audio is recorded for a maximum of 5 seconds before the call moves to Part 2
If the caller does nothing, after 15 seconds,  http://roelofvandijk.com/mp33/IVR/Thank-You-IVR.mp3  is played and the call is ended

Part 2 - mp3=http://roelofvandijk.com/mp33/IVR/ThanksComments.mp3
Audio is recorded and saved as =  Part-2.mp3
If the caller does say something the audio is recorded for a maximum of 10 seconds before the call moves to Part 3
If the caller does nothing, after 15 seconds http://roelofvandijk.com/mp33/IVR/Thank-You-IVR.mp3  is played and the call is ended

Part 3 - mp3_Audio 'http://roelofvandijk.com/mp33/IVR/PNGK-speakOrEndCall.mp3 
    If caller presses 1 the call is transferred (perhaps by using a conference call?) to a new number
    If the caller presses any other key the call is ended

Part 4, Connecting - 
    http://roelofvandijk.com/mp33/IVR/CallingInformation.mp3 is playing for the caller while the other phone is being called
If the other phone does not pick up, that is recorded and http://roelofvandijk.com/mp33/IVR/NoAnswer.mp3 is played, the call is then terminated
If the other party picks up, they can talk for as long as they like, 
if either party hangs up, the call is ended. 


# Implemented

This is a Django app build using Twillio Api.

Functionalities implemented.
1. Takes the call and ask the caller for his country and name.
    1. Prompt the caller to record a message about the purpose of the call or comment about anything.
2. Prompt to press button to forward call to specific number.
3. Forwards call to that number.
    1. If call is not picked it would play an audio file to let caller know that the person is not available right now and he would be contacted back shortly.
    2. If the call is not piked it would also send a message and email to whom the call was forwarded with contact details of caller to contact him back.


Things needed to Use this project.
Python Django
Twillio public API key
Twillio private API key
