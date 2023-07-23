import re
import requests
import telebot
from bs4 import BeautifulSoup

from main import bot, all_commands, states

url: str = 'https://www.1secmail.com/api/v1/'
email = {}


def generator_random_mail(count: int):
    random_mail: str = f'?action=genRandomMailbox&count={count}'
    request = requests.get(url+random_mail)
    list_mails: list = request.json()
    return list_mails


def active_domains():
    active_domain: str = '?action=getDomainList'
    request = requests.get(url+active_domain)
    list_domains: list = request.json()
    return list_domains


def check_mailbox(login: str, domain: str):
    check_emails = f'?action=getMessages&login={login}&domain={domain}'
    request = requests.get(url+check_emails)
    list_emails = request.json()
    return list_emails


def fetching_message(login: str, domain: str, id: str):
    fetch_message = f'?action=readMessage&login={login}&domain={domain}&id={id}'
    request = requests.get(url+fetch_message)
    data_message = request.json()
    text: str = f'''
id message: {data_message['id']}
From: {data_message['from']}
Subject: {data_message['subject']}
Date: {data_message['date']}
Attachments: {data_message['attachments']}
Body: {data_message['body']}
TextBody: {data_message['textBody']}
HTMLBody: {data_message['htmlBody']}
'''
    return text


# Finish it later.
def attachment_download(login: str, domain: str, id: str, file_name: str):
    attch_down = f'?action=download&login={login}&domain={domain}&id={id}&file={file_name}'


markup_Change_temp_mail = telebot.types.InlineKeyboardMarkup()
markup_Change_temp_mail.row(
    telebot.types.InlineKeyboardButton('Refresh', callback_data='click_Refresh_email'),
    telebot.types.InlineKeyboardButton('Done', callback_data='click_Done_email'))

markup_Check_mailbox = telebot.types.InlineKeyboardMarkup()
markup_Check_mailbox.row(
    telebot.types.InlineKeyboardButton('Check mailbox', callback_data='click_Check_mailbox')
)


@bot.message_handler(commands=['anonim_mail'])
def anonim_mail_command(message):
    mail: str = generator_random_mail(1)[0]
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'anonim_mail':
        bot.send_message(message.chat.id, "The command are already being executed")
    else:
        states[chat_id] = 'anonim_mail'
        email[chat_id] = mail
        bot.send_message(message.chat.id, f"Your temp mail: {email[chat_id]}", reply_markup=markup_Change_temp_mail)


@bot.message_handler(func=lambda message: (states.get(message.chat.id) in ['anonim_mail']
                                           and message.text not in all_commands))
def else_message_anonim_mail(message):
    chat_id = message.chat.id
    if chat_id in states and states[chat_id] == 'anonim_mail':
        login, domain = email[chat_id].split('@')
        fetch_message = fetching_message(login, domain, message.text)
        soup = BeautifulSoup(fetch_message, "html.parser")
        text = soup.get_text()
        bot.send_message(message.chat.id, re.sub(r'\n\s*\n', '\n', text))


@bot.callback_query_handler(func=lambda call: states.get(call.message.chat.id) in ['anonim_mail'])
def callback_handler(call):
    chat_id = call.message.chat.id
    login, domain = email[chat_id].split('@')
    try:
        if call.data == 'click_Refresh_email':
            mail: str = generator_random_mail(1)[0]
            email[chat_id] = mail
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Your temp mail: {mail}", reply_markup=markup_Change_temp_mail)
        elif call.data == 'click_Done_email':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Done!\nYour temp mail: {email[chat_id]}", reply_markup=markup_Check_mailbox)
        elif call.data == 'click_Check_mailbox':
            if not check_mailbox(login, domain):
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"Mailbox empty", reply_markup=markup_Check_mailbox)
            else:
                full_text: str = ''
                for dic_message in check_mailbox(login, domain):
                    id_text = f"id: ```{str(dic_message['id'])}```"
                    text = f"""
From: {dic_message['from']}
Subject: {dic_message['subject']}
Date: {dic_message['date']}

"""
                    full_text += id_text + text
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=full_text+'Send the message "id" to display the content.',
                                      reply_markup=markup_Check_mailbox, parse_mode='Markdown')
    except Exception:
        pass
