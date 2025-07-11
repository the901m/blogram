# Blogram: Sync Your Notes to Telegram

Blogram is a Python bot designed to **automatically synchronize your local, folder-based Markdown notes to a Telegram channel**. It ensures your notes stay up-to-date by detecting additions, removals, and modifications, and even provides a neat tree-like representation of your folder structure directly in Telegram.

---

## Why Use Blogram?

* **Effortless Sharing:** Publish your personal knowledge base, course materials, or project documentation to a private or public Telegram channel with minimal setup.
* **Always Up-to-Date:** Focus on writing your notes; Blogram handles the synchronization, reflecting any changes in real-time.
* **Navigable Structure:** Your Telegram channel will mirror your local folder hierarchy, making it easy for you and others to browse your content.
* **Version Control (Informal):** While not a formal VCS, the synchronization provides a historical record of your notes within Telegram's message history.

---

## Getting Started

Follow these steps to set up and run Blogram:

### 1. Prerequisites

* **Python 3.x:** Ensure you have Python 3 installed.
* **Telegram Accounts:** You'll need a Telegram user account to generate API credentials and a bot token from BotFather.

### 2. Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/tho901m/blogram.git
    cd blogram
    ```
2.  **Create and Activate a Virtual Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows, use `.\.venv\Scripts\activate`
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Obtain Telegram API Credentials and Bot Token:**
    * **API ID and API Hash:** Follow [Telethon's guide](https://docs.telethon.dev/en/stable/basic/signing-in.html#signing-in) to get these from my.telegram.org.
    * **Bot API Key:** Create a new bot by chatting with [@BotFather](https://t.me/BotFather) and obtain its API token.
5.  **Create a Credential File:**
    Create a new file (e.g., `credentials.txt`) in the root of the `blogram` directory. This file must contain your credentials on three separate lines, **in this specific order**:

    ```
    YOUR_API_ID
    YOUR_API_HASH
    YOUR_BOT_API_KEY
    ```
    * **Security Note:** Keep this file secure and **never commit it to public repositories**. Consider using environment variables for production deployments.

### 3. Usage

Run the bot from the directory where your notes are located, or provide the full path to your notes folder.

```bash
# Display help message
(.venv) $ python3 main.py --help
````

**Example Run:**

To sync notes from `./my_notes` to a channel `@my_notes_channel`, using `credentials.txt` and `blogram.db` as the database:

Bash

```
(.venv) $ python3 main.py -c credentials.txt -i "@my_notes_channel" -d blogram.db ./my_notes
```

**Command Line Arguments:**

- **`folder` (positional):** Path to the main folder containing your Markdown notes.
    
- **`-c`, `--credential_file`:** Path to your credential file (e.g., `credentials.txt`).
    
- **`-i`, `--channel_id`:** The ID of your Telegram channel (e.g., `"@your_channel_name"`). The `@` is required.
    
- **`-d`, `--database_file`:** (Optional) Path to the database file. If not provided, `main_data.db` will be created in the directory where `main.py` is executed.
    

### 4. How it Works (Under the Hood)

Blogram maintains a local database to track the state of your notes (file paths, Telegram message IDs, content hashes). When you run the bot:

- It scans your specified folder for `.md` files.
    
- For new files, it uploads them as Telegram messages.
    
- For modified files, it updates the corresponding Telegram message.
    
- For deleted files, it removes the associated message from the channel.
    
- Finally, it generates and sends an updated "tree" view of your notes folder structure with links to the respective Telegram messages.
    

---

## Examples & Live Demo

### Console Output Example:

Bash

```
# (Initial run, adding new files)
(.venv) $ python3 main.py -c credential.txt -i "@r_fmhy" -d main.db ./test
[] # Database content before sync
['./test/test.md', './test/test2.md', './test/folder1/1.md', './test/folder1/folder2/2.md'] # Detected folder contents
./test/test.md added
./test/test2.md added
./test/folder1/1.md added
./test/folder1/folder2/2.md added
└──l [folder2]()
    └──l [2](https://t.me/r_fmhy/2396)
# ... (subsequent tree outputs and database updates)
[('./test/folder1/folder2', '2.md', 2396, 'f1448a27063bc632942e48b8170a5cb8567199d8'), ...] # Final database content
```

### Telegram Channel Output:

Blogram will post your Markdown files as messages and then a structured file tree. You can view a live example of the format and output on the [@r_fmhy Telegram channel](https://t.me/r_fmhy).

---

## Known Limitations

- **Markdown Formatting Discrepancies:** Italic and strikethrough formatting may not render correctly due to limitations with the current Telethon version's Markdown support. This is expected to be resolved with the release of Telethon v2, which will support [CommonMark's Markdown](https://commonmark.org/).
    

---

## Future Enhancements (TODO)

- **Automated Pinning:** Automatically pin the tree message to the channel.
    
- **Change Log Report:** Provide a summary of changes (additions, modifications, deletions) after each synchronization run.
    
- **Inter-file Link Resolution:** Handle links between `.md` files within the Telegram channel, allowing for seamless navigation.
    
- **Table of Contents Generation:** Automatically generate a navigable table of contents for larger note sets.
    
- **Pandoc Integration:** Extend support to other document formats (e.g., HTML, PDF) via Pandoc integration.
