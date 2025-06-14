# Telegram Userbot Keyword Listener

A simple and efficient Telegram userbot built with Telethon. This bot listens to all messages in chats, groups, and channels that your user account is a member of, and prints messages containing a specific keyword (default: `target`) to the terminal.

## Features
- Listens to all incoming messages your user account can see
- Prints messages containing the keyword `target` to the terminal
- Easy to configure and extend for other keywords or actions

## Setup
1. **Clone this repository**
2. **Install dependencies**
   ```bash
   pip install telethon
   ```
3. **Get your Telegram API credentials**
   - Visit https://my.telegram.org
   - Log in and create a new application to get your `api_id` and `api_hash`
4. **Configure your credentials**
   - Edit `main.py` and set your `api_id` and `api_hash`
5. **Run the bot**
   ```bash
   python main.py
   ```
6. **Login**
   - Enter your phone number and the code sent to your Telegram app

## Usage
- The bot will print to the terminal any message containing the keyword `target` from any chat, group, or channel your user account is a member of.
- You can change the keyword in `main.py` by editing the line:
  ```python
  if event.text and 'target' in event.text.lower():
  ```

## Notes
- This is a userbot, not a regular Telegram bot. It uses your personal Telegram account.
- Make sure to comply with Telegram's Terms of Service. Using userbots may risk your account if abused.
- For private channels, your user account must be a member to see messages.

## License
MIT 