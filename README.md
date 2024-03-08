# Chat-Room
Chatroom for real time messageing and file transfer

STEPS:

1. Run the SERVER program
2. Run the CLIENT program in another terminal on the same system
3. The first CLIENT to join a SERVER can set a PASSWORD for the SERVER
4. All other CLIENTS joining the same SERVER must enter the right PASSWORD
5. Multiple CLIENTS can join the same SERVER (room) and group chat with one another
6. Each CLIENT must choose an ALIAS
7. There is NO mechanism in place to check for DUPLICATE ALIASES as of now. Ensure all ALIASES are UNIQUE
8. To send a MESSAGE, type it in normally
9.  Do NOT BEGIN with the ':' character
10. To EXIT the room enter ':Exit'
11. To send a FILE enter ':<FILENAME>'
12. Ensure the FILE is in the SAME DIRECTORY as the CLIENT program sending it
13. Ensure CLIENTS are present in DIFFERENT DIRECTORIES to prevent reading and writing the same file
