# Face recognition on Raspberry Pi

This software runs on a Raspberry Pi equipped with a camera, and allows to recognize people using Face Recognition AI and to update a list of participants (Google Sheet) to an event. When a person is recognized, his/her name is looked up in the list of participants and he/she is marked as present.

The software also allows people to register to the system, for them to be recognized during further executions. A picture is taken from the user, and its facial features are extracted and stored in an online database.

# Execution

Run the following commands on the Raspberry Pi equpied with a camera :

```
cd src
python main.py
```
