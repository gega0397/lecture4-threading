Program utilizes threading module to send multiple concurrent API requests and save output to a json file.

program can be run with extra arguments:
* flag -s: Flag to indicate whether to use semaphore
* flag -n: Number of semaphore

if -s is not profivded the script spawns 100 threads, 1 thread for each request.
