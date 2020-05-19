# SCP-079-STATUS

This bot is used to check Linux server status.

## How to use

- Read [the document](https://scp-079.org/status/) to learn more
- [README](https://scp-079.org/readme/) of the SCP-079 Project's demo bots
- Discuss [group](https://t.me/SCP_079_CHAT)

## Requirements

- Python 3.6 or higher
- pip: `pip install -r requirements.txt` 
- or pip: `pip install -U APScheduler psutil pyrogram pyyaml tgcrypto`

## Files

- languages
   - `cmn-Hans.yml` : Mandarin Chinese (Simplified)
- plugins
    - functions
        - `channel.py` : Functions about channel
        - `command.py` : Functions about command
        - `config.py` : Functions about group settings
        - `decorators.py` : Some decorators
        - `etc.py` : Miscellaneous
        - `file.py` : Save files
        - `filters.py` : Some filters
        - `group.py` : Functions about group
        - `ids.py` : Modify id lists
        - `receive.py` : Receive data from exchange channel
        - `telegram.py` : Some telegram functions
        - `timers.py` : Timer functions
        - `user.py` : Functions about user and channel object
    - handlers
        - `command.py` : Handle commands
    - `glovar.py` : Global variables
- `.gitignore` : Ignore
- `config.ini.example` -> `config.ini` : Configuration
- `LICENSE` : GPLv3
- `main.py` : Start here
- `README.md` : This file
- `requirements.txt` : Managed by pip

## Contribute

Welcome to make this project even better.

If you are willing to contribute, please [apply](https://t.me/SCP_079_TICKET_BOT) to join our private group on GitLab.

## Translation

- [Choose Language Tags](https://www.w3.org/International/questions/qa-choosing-language-tags)
- [Language Subtag Registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry)

## License

Licensed under the terms of the [GNU General Public License v3](LICENSE).
