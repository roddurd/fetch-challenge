# fetch-challenge
Backend coding challenge for Fetch: "Receipt Processor"

## Requirements
Make sure Docker is installed on your system. You can get Docker [here](https://docs.docker.com/get-docker/).

If you're on a Windows machine, make sure you have WSL (Windows Subsystem for Linux) installed.
You can run `wsl --update` in Command Prompt to ensure it's installed and up-to-date.

## Usage
After cloning this repository, open up a terminal in the `fetch-challenge/` directory.

Run `docker build -t fetch .`.

Then run `docker run -p 5000:5000 fetch`.

The API is now exposed on `http://localhost:5000/`.
