from telethon import TelegramClient
from telethon.errors import EntityBoundsInvalidError

import asyncio
import os
import hashlib
import markdown
import sqlite3
import argparse

def get_args():
    # Create the parser
    parser = argparse.ArgumentParser(description='Send and handle changes in .md files in a folder to Telegram')

    # Add optional database file argument
    parser.add_argument('-d', '--database_file', type=str, 
                        help='Path to the database file (optional). If not provided, a default database in main folder will be created.')

    # Add required credential file argument
    parser.add_argument('-c', '--credential_file', type=str, 
                        help='Path to the credential file containing account information. The credential file must contain 3 lines for API_ID, API_HASH and API_KEY in order.')

    # Add required credential file argument
    parser.add_argument('-i', '--channel_id', type=str, 
                        help='Id of the channel. for example "@example" (@ is required)')

    # Add positional argument for the folder
    parser.add_argument('folder', type=str, 
                        help='Path of the main folder')

    # Parse the arguments
    args = parser.parse_args()

    # Check if the database file is provided, otherwise create a default one
    if args.database_file:
        database_file = args.database_file
    else:
        database_file = os.path.join(args.folder, 'main_data.db')

    args.database_file = database_file

    # Check if the specified folder exists
    if not os.path.exists(args.folder):
        raise FileNotFoundError(f'The specified folder does not exist: {args.folder}')

    return args  # Return the parsed arguments

if __name__ == '__main__':
    try:
        global arguments
        arguments = get_args()  # Store the returned arguments
    except FileNotFoundError as e:
        print(e)
        exit(1)

with open(arguments.credential_file, 'r') as file:
    lines = file.readlines()
    # Strip whitespace and ensure there are at least 3 lines
    if len(lines) < 3:
        raise ValueError("The credential file must contain at least 3 lines for API_ID, API_HASH, and API_KEY.")

    API_ID = lines[0].strip()  # First line
    API_HASH = lines[1].strip()  # Second line
    API_KEY = lines[2].strip()  # Third line


bot = TelegramClient("bot", API_ID, API_HASH)

chatid = arguments.channel_id


def file_to_markdown(path):

    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as file:
            converted = markdown.get_telethon_markdown(file.read())

    else:
        converted = markdown.get_telethon_markdown(path)
    return converted


async def send_message(text):
    await bot.start(bot_token=API_KEY)
    texts = file_to_markdown(text)
    messages = []
    for item in texts:
        try:
            msg = await bot.send_message(
                chatid, item, link_preview=False, parse_mode="markdown"
            )
            messages.append(msg.id)

        except EntityBoundsInvalidError:
            print("there was an error in: ", item)
            pass

        # sleep is because of telegram limitations
        await asyncio.sleep(3)

    await bot.disconnect()
    return messages


async def remove_message(path, db_entries):
    await bot.start(bot_token=API_KEY)
    list_of_msg_id = []
    indexNumber_of_next_msg = 0
    message_id = 0

    # append faq message_id, it's needed for deleting the last message or faq messages 
    list_of_msg_id.append(
        [i for i in cur.execute("SELECT message_id FROM faq ORDER BY message_id")][0][0]
    )

    # append reqular message_id
    for file in db_entries:
        list_of_msg_id.append(file[2])
        if file[0] + "/" + file[1] == path:
            message_id = file[2]

    # find next message index number
    for msg_id in sorted(list_of_msg_id):
        indexNumber_of_next_msg += 1
        if msg_id == message_id:
            break

    await bot.delete_messages(
        chatid, range(message_id, sorted(list_of_msg_id)[indexNumber_of_next_msg])
    )


def get_link_from_path(path):
    if os.path.isdir(path):
        db_entries = [i for i in cur.execute("SELECT path,message_id FROM faq")]
        for database_path in db_entries:
            if path == database_path[0]:
                print(path, db_entries)

                return "https://t.me/" + chatid[1:] + "/" + str(database_path[1])

    else:
        db_entries = [i for i in cur.execute("SELECT * FROM main ORDER BY path ,file")]
        for database_path in db_entries:
            if path == os.path.join(database_path[0], database_path[1]):
                return "https://t.me/" + chatid[1:] + "/" + str(database_path[2])

    return ""


def path_to_md_tree(path, last=True, header=""):
    elbow = "└──"
    pipe = "│    "
    tee = "├──"
    blank = "    "

    # Initialize an output string

    output = (
        header
        + (elbow if last else tee)

        # the l at the beginning is for rtl languages  
        + f"l [{os.path.splitext(os.path.basename(path))[0]}]({get_link_from_path(path=path)})\n"
    )

    if os.path.isdir(path):
        children = os.listdir(path)
        children.sort()  # Sort children for consistent output
        for i, child in enumerate(children):
            child_path = os.path.join(path, child)
            output += path_to_md_tree(
                child_path,
                last=i == len(children) - 1,
                header=header + (blank if last else pipe),
            )

    return output


def compute_sha1(file_path):
    sha1_hash = hashlib.sha1()  # Create a new SHA-1 hash object
    with open(file_path, "rb") as f:  # Open the file in binary mode
        # Read the file in chunks to avoid using too much memory
        for byte_block in iter(lambda: f.read(4096), b""):
            sha1_hash.update(byte_block)  # Update the hash with the bytes read
    return sha1_hash.hexdigest()  # Return the hexadecimal representation of the hash


main_file = []

con = sqlite3.connect(arguments.database_file)
cur = con.cursor()

cur.execute(
    "CREATE TABLE IF NOT EXISTS main(path,file,message_id INTIGER DEFAULT 0,file_hash)"
)

cur.execute("CREATE TABLE IF NOT EXISTS faq(path,message_id INTIGER DEFAULT 0)")


db_entries = [i for i in cur.execute("SELECT * FROM main ORDER BY path ,file")]


def insert_to_database(path, message):
    cur.executemany(
        "INSERT INTO main(path,file,message_id,file_hash) VALUES(?,?,?,?)",
        [
            [
                os.path.dirname(path),
                os.path.basename(path),
                message[0],
                compute_sha1(path),
            ]
        ],
    )
    con.commit()


def insert_to_faq(path, message):
    cur.executemany(
        "INSERT INTO faq(path,message_id) VALUES(?,?)",
        [
            [
                path,
                message[0],
            ]
        ],
    )
    con.commit()


def update_the_database(path, message):
    # print(message[0], type(message[0]))
    cur.executemany(
        "UPDATE main SET message_id = ?, file_hash = ? WHERE path = ? AND file = ?",
        [
            [
                message[0],
                compute_sha1(path),
                os.path.dirname(path),
                os.path.basename(path),
            ]
        ],
    )
    con.commit()


def delete_from_database(path):
    cur.executemany(
        "DELETE FROM main WHERE path = ? AND file = ?",
        [[os.path.dirname(path), os.path.basename(path)]],
    )
    con.commit()


def delete_from_faq():
    cur.execute("DELETE FROM faq")
    con.commit()


async def faq_message_handling(change_signal):
    if change_signal != 0:
        await bot.start(bot_token=API_KEY)
        # remove faq messages
        db_entries = [
            i for i in cur.execute("SELECT message_id FROM faq ORDER BY message_id")
        ]
        try:
            await bot.delete_messages(
                chatid, range(db_entries[0][0], db_entries[::-1][0][0] + 1)
            )
        except IndexError:
            pass

        delete_from_faq()

        db_entries = [
            i for i in cur.execute("SELECT DISTINCT path FROM main ORDER BY path DESC")
        ]
        # tree, send and insert
        for path in db_entries:
            tree = path_to_md_tree(path[0])
            print(tree)
            message = await send_message(tree)

            print(path)
            insert_to_faq(path[0], message)
            insert_to_faq(path[0], message[::-1])


async def main(main_folder_path):
    change_signal = 0

    database_files_path = []
    for file in db_entries:
        database_files_path.append(os.path.join(file[0], file[1]))
    print(database_files_path)

    system_files_path = []
    for path, folder, files in os.walk(main_folder_path):
        for file in files:
            filename, file_extention = os.path.splitext(file)
            if file_extention == ".md":
                system_files_path.append(os.path.join(path, file))
    print(system_files_path)

    for path in system_files_path:
        if path not in database_files_path:
            print(path, "added")
            # send message
            message = await send_message(path)
            # insert the file path into database
            insert_to_database(path, message)
            change_signal += 1

        else:
            # if system hash != database hash: remove message
            for file in db_entries:
                if path == os.path.join(file[0], file[1]) and file[3] != compute_sha1(
                    path
                ):
                    print(path, "modified")
                    # remove message and send again
                    await remove_message(path, db_entries)
                    message = await send_message(path)

                    update_the_database(path, message)
                    change_signal += 1

    for path in database_files_path:
        if path not in system_files_path:
            print(path, "deleted")
            # remove message
            await remove_message(path, db_entries)
            # remove from database
            delete_from_database(path)
            change_signal += 1

    await faq_message_handling(change_signal)

    print([i for i in cur.execute("SELECT * FROM main ORDER BY path DESC")])


# con.close()

asyncio.run(main(arguments.folder))
