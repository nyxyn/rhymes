import hexchat
import threading
import requests

CHANNEL_EVENT = 'Channel Message'
SELF_EVENT = 'Your Message'
KEYWORD = '.rhyme'
CHANNEL_KEY = 'channel'
API_URL = 'https://api.datamuse.com/words?rel_rhy={}'
MAX_RESULT_COUNT = 3

__module_name__ = 'rhyme'
__module_version__ = '1.0'
__module_description__ = 'Get rhymes'


def get_rhymes(query):
    response = requests.get(API_URL.format(query)).json()
    rhymes = []

    for rhyme in response:
        rhymes.append(rhyme['word'])

        if len(rhymes) == MAX_RESULT_COUNT:
            break

    return rhymes


def say(channel, query):
    channel_context = hexchat.find_context(channel=channel)
    rhymes = get_rhymes(query)

    rhymes_command = 'msg {} <RhymeZilla>: {}'.format(channel, rhymes)
    channel_context.command(rhymes_command)


def print_callback(words, eol, userdata):
    message = words[1].lower()
    channel = hexchat.get_info(CHANNEL_KEY)

    if KEYWORD in message:
        parts = message.split(' ')

        if len(parts) >= 2:
            key = parts[0]
            query = parts[1]

            thread = threading.Thread(target=say, args=(channel, query))
            thread.start()

    return hexchat.EAT_NONE


hexchat.prnt('Setting hook for rhymes...')
hexchat.hook_print(CHANNEL_EVENT, print_callback)
hexchat.hook_print(SELF_EVENT, print_callback)
hexchat.prnt('Hook set')

