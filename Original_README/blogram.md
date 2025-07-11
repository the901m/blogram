# blogram
imagine you want to share your notes which are organized in folder based structure into a telegram channel. This bot handles everything for you, just give it the folder.
If you perform any changes to your notes (add/remove/modify), it will keep the content up to date. also at the end it will send your folder structure like a tree command.

## usage
1. clone the repository and cd into it
2. [create a virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) in python, activate it and `pip install -r requirements.txt`
3. create a file for your credentials. The credential file must contain 3 lines for *API_ID*, *API_HASH*, and *API_KEY*  **in order**.
4. for running the code: `python main.py --help`
- get API_ID and API_HASH like [this](https://docs.telethon.dev/en/stable/basic/signing-in.html#signing-in), and API_KEY from [botfather](https://t.me/BotFather).
- you have to run the code from the same folder as your notes.
## example
#### help message:
```bash
(.venv) $ python3 main.py --help
usage: main.py [-h] [-d DATABASE_FILE] [-c CREDENTIAL_FILE] [-i CHANNEL_ID] folder

Send and handle changes in .md files in a folder to Telegram

positional arguments:
  folder                Path of the main folder

options:
  -h, --help            show this help message and exit
  -d, --database_file DATABASE_FILE
                        Path to the database file (optional). If not provided, a default database in main folder will be created.
  -c, --credential_file CREDENTIAL_FILE
                        Path to the credential file containing account information. The credential file must contain 3 lines for
                        API_ID, API_HASH and API_KEY in order.
  -i, --channel_id CHANNEL_ID
                        Id of the channel. for example "@example" (@ is required)
```
#### running the bot:
```bash
(.venv) $ python3 main.py -c credential.txt -i "@r_fmhy" -d main.db ./test
[] # this is the content of your database
['./test/test.md', './test/test2.md', './test/folder1/1.md', './test/folder1/folder2/2.md'] # these are your folder contents
./test/test.md added
./test/test2.md added
./test/folder1/1.md added
./test/folder1/folder2/2.md added
└──l [folder2]()
    └──l [2](https://t.me/r_fmhy/2396)

('./test/folder1/folder2',) # created tree for this folder
./test/folder1/folder2 [('./test/folder1/folder2', 2397), ('./test/folder1/folder2', 2397)]
└──l [folder1]()
    ├──l [1](https://t.me/r_fmhy/2395)
    └──l [folder2](https://t.me/r_fmhy/2397)
        └──l [2](https://t.me/r_fmhy/2396)

('./test/folder1',)
./test/folder1 [('./test/folder1/folder2', 2397), ('./test/folder1/folder2', 2397), ('./test/folder1', 2398), ('./test/folder1', 2398)]
./test/folder1/folder2 [('./test/folder1/folder2', 2397), ('./test/folder1/folder2', 2397), ('./test/folder1', 2398), ('./test/folder1', 2398)]
└──l [test]()
    ├──l [folder1](https://t.me/r_fmhy/2398)
    │    ├──l [1](https://t.me/r_fmhy/2395)
    │    └──l [folder2](https://t.me/r_fmhy/2397)
    │        └──l [2](https://t.me/r_fmhy/2396)
    ├──l [test](https://t.me/r_fmhy/2393)
    └──l [test2](https://t.me/r_fmhy/2394)

('./test',)
[('./test/folder1/folder2', '2.md', 2396, 'f1448a27063bc632942e48b8170a5cb8567199d8'), ('./test/folder1', '1.md', 2395, '65a09068bae1e56e28af86f50b3a35fffb0e6178'), ('./test', 'test.md', 2393, '338af1a2325613afe01077ca60c4c6c21b16e1d5'), ('./test', 'test2.md', 2394, '840f16c7a6c89b1f2731eda9bdc20d078ce78360')] # your database content at the end
```
#### results in telegram:
![[Pasted image 20250711070743.png]]

- you can also check [@r_fmhy](https://t.me/r_fmhy) channel to see the format.

## known issue
- the italic and strikethrough doesn't work, it would be fixed when the telethon v2 releases. it would have support [CommonMark's markdown](https://commonmark.org/).

## TODO
- [ ] main faq message should automatically get pinned
- [ ] change report (what where added)
- [ ] handle links between .md files.
- [ ] table of content
- [ ] pandoc implementation to support other doc formats 
