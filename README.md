## Test project for DrWeb. HTTP API
### Description
File storage with HTTP API access

It is a daemon with HTTP API server for uploading, downloading and deleting files.

Upload:
Once the server receives a file from the client, it returns the file’s hash in the http response field.
The server puts the file in store/ab/abcdef12345 where «abcdef12345» is the file name (matches its hash), and /ab/ is the subdirectory name (matches the first two hash symbols).

Download:
Once the server receives a download request with the file’s hash, it looks for the file in the local storage and returns it if found. 

Delete:
Once the server receives a deletion request with the file’s hash, it looks for the file in the local storage and deletes it if found. 

### Dependencies

- Python 3.8

### Installation
- 'git clone https://github.com/DrYshio/DrWebTestAPI.git'
- 'pip install requirements.txt'
- Change variable PATH_TO_WORKING_DIRECTORY in config.py to the path where you need store directory to be created.
- Change [user] and [path to project directory] in api_server.service
- Place api_server.service in /etc/systemd/system/
- '$ systemctl daemon-reload'
- '$ sudo systemctl restart api_server'
- (optional) '$ systemctl status api_server'
- Follow the link 127.0.0.1:8000/docs

