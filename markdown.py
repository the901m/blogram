# TODO: main functionality, handle headers, bolding, italic, streak line, underline,
import re
from typing import List


def header_number_to_emoji(text):
    markdown_text = text

    header_emojis = {
        1: "1️⃣",  # Level 1 header
        2: "2️⃣",  # Level 2 header
        3: "3️⃣",  # Level 3 header
        4: "4️⃣",  # Level 4 header
        5: "5️⃣",  # Level 5 header
        6: "6️⃣",  # Level 6 header
    }

    for level in range(1, 7):
        pattern = f"^({level*'#'}) (.*)"
        replacement = f"{header_emojis[level]}  \\1"
        markdown_text = re.sub(
            pattern,
            f"{header_emojis[level]} **\\2**",
            markdown_text,
            flags=re.MULTILINE,
        )

    return markdown_text


def split_text_by_lines(text: str, max_len: int = 4090) -> List[str]:
    """
    Split `text` into chunks of at most `max_len` characters.
    Cuts only at line boundaries. If a single line exceeds max_len,
    it will be hard-split into max_len-sized pieces.
    Returns a list of text chunks (with newline chars preserved).
    """
    chunks: List[str] = []
    buffer: List[str] = []
    buf_len = 0

    for line in text.splitlines(keepends=True):
        L = len(line)

        # If one line alone is too long, flush buffer and hard-split it:
        if L > max_len:
            if buffer:
                chunks.append("".join(buffer))
                buffer, buf_len = [], 0
            # hard-split the long line
            for start in range(0, L, max_len):
                chunks.append(line[start : start + max_len])
            continue

        # If adding this line would overflow, flush buffer first:
        if buf_len + L > max_len:
            chunks.append("".join(buffer))
            buffer, buf_len = [line], L
        else:
            buffer.append(line)
            buf_len += L

    # Flush any remainder
    if buffer:
        chunks.append("".join(buffer))

    return chunks


def get_telethon_markdown(text):
    text = header_number_to_emoji(text)
    list_of_text = split_text_by_lines(text)
    return list_of_text


# TODO: toc
