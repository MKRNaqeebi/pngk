# pngk

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
