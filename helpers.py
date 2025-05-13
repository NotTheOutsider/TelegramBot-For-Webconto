import re
import textwrap
from datetime import datetime

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