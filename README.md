# Glitchat

## Running

Start with cloning the repository and installing dependencies:

```bash
$ git clone https://github.com/srijal30/genuine-djinn.git
$ python3 -m pip install -r requirements.txt
```

Now, to start the app run the following:

```bash
$ python3 main.py -a app
```

### Running Server

If you want to run your own server instead of the default one, you first need to setup the database.

**Note:** This assumes you already have postgres installed.

```bash
$ echo DB_SERVER=postgresql://postgres:postgres@localhost:5432/ > .env
$ python3 -m venv .venv # a venv is required for prisma to work properly
$ source .venv/bin/activate
$ npm i -g prisma # this is only if prisma isnt already installed
$ prisma db push
$ python3 -m prisma generate
```

You can then run the server like so:

```bash
$ python3 main.py -a server
```
