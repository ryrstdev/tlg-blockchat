import asyncio
import io
import json
import logging

import openai
from src.utils import (
    LOG_PATH,
    num_tokens_from_messages,
    read_existing_conversation,
)
from telethon.events import NewMessage
from unidecode import unidecode

# Functions for bot operation

async def clearmsg(event: NewMessage) -> str:
    try:
        #cmd = event.text.split(" ", maxsplit=1)[1]
        cmd = f"mv -f log/chats/{event.text}* log/archive/"
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        e = stderr.decode()
        if not e:
            e = "No Error"
        o = stdout.decode()
        if not o:
            o = "Clear succeeded."
        else:
            _o = [f"`  {x}`" for x in o.split("\n")]
            o = "\n".join(_o)
        OUTPUT = (f"Blocky says ")
        if len(OUTPUT) > 4095:
            with io.BytesIO(str.encode(OUTPUT)) as out_file:
                out_file.name = "exec.text"
                await event.client.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption=cmd,
                )
                await event.delete()
        logging.debug("Clear initiated")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    return OUTPUT
