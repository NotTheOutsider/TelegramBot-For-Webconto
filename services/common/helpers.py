import re
import textwrap
from datetime import datetime
from secrets import randbelow, token_urlsafe

def escape_markdown_v2(text):
    if text is None:
        return ""
    reserved_chars = r'([_\*\[\]\(\)~`>\#\+\-=\|\{\}\.!])'
    return re.sub(reserved_chars, r'\\\1', str(text))

def generate_tg_mssg(params: dict):
         
    mssg = textwrap.dedent(f'''\
        Организация: {params.get('organisation')}
        Пользователь: {params.get('user')}
        Физ. лицо: {params.get('individual') if params.get('individual') != '' else 'Не указан'}
        Телефон: {params.get('tel')}
        Email: {params.get('email') if params.get('email') != '' else 'Не указан'}
        ——————————————————
        ==Баг==
        {params.get('message')}
        <Объект>
        {params.get('object') if params.get('email') != '' else 'Не указан'}
        
        {datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}
        {params.get('release')}
        {params.get('platform')}''')
    
    mssg = '\n'.join([m.lstrip() for m in mssg.split('\n')])
        
    mssg = escape_markdown_v2(mssg)

    return mssg

def generate_verification_code():
    return f"{randbelow(1000000):06d}"

def generate_chat_mask():
    return token_urlsafe(16)