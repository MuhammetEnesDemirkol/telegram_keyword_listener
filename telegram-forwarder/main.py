# Main script for Telegram Userbot
# This file will contain the main logic for the auto-forwarding bot

from telethon import TelegramClient, events
from config import api_id, api_hash
import os
import re
import json
from datetime import datetime

SESSION_DIR = 'sessions'
if not os.path.exists(SESSION_DIR):
    os.mkdir(SESSION_DIR)

# Logs klasörünün varlığını kontrol et
LOGS_DIR = 'logs'
if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)

def log_error(message):
    with open('logs/forward.log', 'a') as f:
        f.write(f"[{datetime.now()}] {message}\n")

# Render için sabit session ismi kullan
session_name = 'user'
client = TelegramClient(os.path.join(SESSION_DIR, session_name), api_id, api_hash)

# OWNER_ID'yi settings.json'dan oku
def get_owner_id():
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            return settings.get('owner_id')
    except:
        return None

def save_owner_id(user_id):
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
    except:
        settings = {}
    
    settings['owner_id'] = user_id
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

async def main():
    await client.start()
    print("✅ Telegram oturumu başarıyla başlatıldı.")
    
    # settings.json dosyasını oku
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    
    source_channel = settings.get('source_channel')
    target_channel = settings.get('target_channel')
    
    # İlk mesajı gönderen kişiyi owner olarak kaydet
    @client.on(events.NewMessage(pattern='/start'))
    async def start_handler(event):
        user_id = event.sender_id
        save_owner_id(user_id)
        await event.respond(f"Merhaba! Bot başlatıldı ve siz owner olarak ayarlandınız (ID: {user_id})")
        print(f"Owner ID ayarlandı: {user_id}")
    
    # Komut sistemi
    @client.on(events.NewMessage(pattern='/setsource'))
    async def set_source(event):
        owner_id = get_owner_id()
        if not owner_id:
            await event.respond("Lütfen önce /start komutunu kullanın.")
            return
        if event.sender_id != owner_id:
            await event.respond("Bu komutu sadece bot sahibi kullanabilir.")
            return
            
        try:
            channel_username = event.text.split()[1]
            if not channel_username.startswith('@'):
                channel_username = '@' + channel_username
            entity = await client.get_entity(channel_username)
            settings['source_channel'] = entity.id
            with open('settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
            await event.respond(f"Kaynak kanal başarıyla ayarlandı: {channel_username}")
            print(f"Kaynak kanal güncellendi: {channel_username} (ID: {entity.id})")
        except Exception as e:
            error_message = f"Kaynak kanal ayarlama hatası: {e}"
            print(error_message)
            log_error(error_message)
            await event.respond(error_message)
    
    @client.on(events.NewMessage(pattern='/settarget'))
    async def set_target(event):
        owner_id = get_owner_id()
        if not owner_id:
            await event.respond("Lütfen önce /start komutunu kullanın.")
            return
        if event.sender_id != owner_id:
            await event.respond("Bu komutu sadece bot sahibi kullanabilir.")
            return
            
        try:
            channel_username = event.text.split()[1]
            if not channel_username.startswith('@'):
                channel_username = '@' + channel_username
            entity = await client.get_entity(channel_username)
            settings['target_channel'] = entity.id
            with open('settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
            await event.respond(f"Hedef kanal başarıyla ayarlandı: {channel_username}")
            print(f"Hedef kanal güncellendi: {channel_username} (ID: {entity.id})")
        except Exception as e:
            error_message = f"Hedef kanal ayarlama hatası: {e}"
            print(error_message)
            log_error(error_message)
            await event.respond(error_message)
    
    @client.on(events.NewMessage(pattern='/setsourceid'))
    async def set_source_id(event):
        owner_id = get_owner_id()
        if not owner_id:
            await event.respond("Lütfen önce /start komutunu kullanın.")
            return
        if event.sender_id != owner_id:
            await event.respond("Bu komutu sadece bot sahibi kullanabilir.")
            return
        try:
            channel_id = int(event.text.split()[1])
            settings['source_channel'] = channel_id
            with open('settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
            await event.respond(f"Kaynak kanal ID ile başarıyla ayarlandı: {channel_id}")
            print(f"Kaynak kanal ID ile güncellendi: {channel_id}")
        except Exception as e:
            error_message = f"Kaynak kanal ID ayarlama hatası: {e}"
            print(error_message)
            log_error(error_message)
            await event.respond(error_message)

    @client.on(events.NewMessage(pattern='/settargetid'))
    async def set_target_id(event):
        owner_id = get_owner_id()
        if not owner_id:
            await event.respond("Lütfen önce /start komutunu kullanın.")
            return
        if event.sender_id != owner_id:
            await event.respond("Bu komutu sadece bot sahibi kullanabilir.")
            return
        try:
            channel_id = int(event.text.split()[1])
            settings['target_channel'] = channel_id
            with open('settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
            await event.respond(f"Hedef kanal ID ile başarıyla ayarlandı: {channel_id}")
            print(f"Hedef kanal ID ile güncellendi: {channel_id}")
        except Exception as e:
            error_message = f"Hedef kanal ID ayarlama hatası: {e}"
            print(error_message)
            log_error(error_message)
            await event.respond(error_message)
    
    @client.on(events.NewMessage(pattern='/status'))
    async def status(event):
        owner_id = get_owner_id()
        if not owner_id:
            await event.respond("Lütfen önce /start komutunu kullanın.")
            return
        if event.sender_id != owner_id:
            await event.respond("Bu komutu sadece bot sahibi kullanabilir.")
            return
            
        source = settings.get('source_channel', 'Ayarlanmamış')
        target = settings.get('target_channel', 'Ayarlanmamış')
        await event.respond(f"📊 Bot Durumu:\n\nKaynak Kanal: {source}\nHedef Kanal: {target}")
    
    @client.on(events.NewMessage(pattern='/listchannels'))
    async def list_channels(event):
        owner_id = get_owner_id()
        if not owner_id:
            await event.respond("Lütfen önce /start komutunu kullanın.")
            return
        if event.sender_id != owner_id:
            await event.respond("Bu komutu sadece bot sahibi kullanabilir.")
            return
        try:
            from telethon.tl.functions.messages import GetDialogsRequest
            from telethon.tl.types import InputPeerEmpty
            dialogs = await client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=200,
                hash=0
            ))
            msg = "\n".join([f"{chat.title}: {chat.id}" for chat in dialogs.chats if hasattr(chat, 'title')])
            await event.respond(f"Üye olunan kanallar ve ID'leri:\n\n{msg}")
        except Exception as e:
            error_message = f"Kanal listesi alınamadı: {e}"
            print(error_message)
            log_error(error_message)
            await event.respond(error_message)
    
    # Mesaj dinlemeye başla ve hedef kanala yönlendir
    @client.on(events.NewMessage)
    async def handler(event):
        if event.text and 'target' in event.text.lower():
            print(f"target bulundu! Chat: {event.chat_id}, Gönderen: {event.sender_id}, İçerik: {event.text}")
        # Eğer kaynak kanal ayarlanmamışsa veya mesaj kaynak kanaldan gelmiyorsa işlem yapma
        if not settings.get('source_channel') or event.chat_id != settings['source_channel']:
            return
            
        print(f"Yeni mesaj alındı: {event.message.text}")
        try:
            if settings.get('target_channel'):
                await client.send_message(settings['target_channel'], event.message.text)
                print(f"Mesaj hedef kanala yönlendirildi: {settings['target_channel']}")
            else:
                print("Hedef kanal ayarlanmamış!")
        except Exception as e:
            error_message = f"Mesaj yönlendirme hatası: {e}"
            print(error_message)
            log_error(error_message)
    
    if source_channel:
        print(f"Kanal {source_channel} için mesaj dinleme başlatıldı.")
    else:
        print("Kaynak kanal henüz ayarlanmamış. /setsource komutu ile ayarlayabilirsiniz.")
    
    print("Bot başlatıldı! Telegram'da /start komutunu kullanarak botu yapılandırabilirsiniz.")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main()) 