# SCP-079-STATUS

With this program, you can easily create a bot to monitor your Linux server's status in the Telegram channel.

## How to use

- [Demo](https://t.me/SCP_079_CRITICAL)
- Read [the document](https://scp-079.org/status/) to learn more
- [README](https://scp-079.org/readme/) of the SCP-079 Project's demo bots
- Discuss [group](https://t.me/SCP_079_CHAT)

## Requirements

- OS: Linux
- Python: 3.7 or higher
- pip: `pip install -r requirements.txt` 

## Files

- data
    - The folder will be generated when program starts
- examples
    - `config.ini` -> `../data/config/config.ini` : Configuration example
    - `report.txt` -> `../data/config/report.txt` : Report template example
- languages
    - `cmn-Hans.yml` : Mandarin Chinese (Simplified)
    - `cmn-Hant-TW.yml` : Mandarin Chinese in Taiwan (Traditional)
    - `en.yml` : English
- plugins
    - functions
        - `command.py` : Functions about command
        - `decorators.py` : Some decorators
        - `etc.py` : Miscellaneous
        - `file.py` : Save files
        - `filters.py` : Some filters
        - `group.py` : Functions about group
        - `program.py` : Functions about program
        - `status.py` : Functions about system status
        - `telegram.py` : Some telegram functions
        - `timers.py` : Timer functions
    - handlers
        - `command.py` : Handle commands
    - `__init__.py`
    - `checker.py` : Check the format of `config.ini`
    - `glovar.py` : Global variables
    - `start.py` : Execute before client start
    - `version.py` : Execute before main script start
- `.gitignore` : Specifies intentionally untracked files that Git should ignore
- `dictionary.dic` : Project's dictionary
- `LICENSE` : GPLv3
- `main.py` : Start here
- `README.md` : This file
- `requirements.txt` : Managed by pip

## Contribution

Contributions are always welcome, whether it's modifying source code to add new features or bug fixes, documenting new file formats or simply editing some grammar.

You can also join the [discuss group](https://t.me/SCP_079_CHAT) if you are unsure of anything.

## Translation

- [Choose Language Tags](https://www.w3.org/International/questions/qa-choosing-language-tags)
- [Language Subtag Registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry)

# Copyright & License

- Copyright (C) 2019-2021 SCP-079 <https://scp-079.org>
- Licensed under the terms of the [GNU General Public License v3](LICENSE).
