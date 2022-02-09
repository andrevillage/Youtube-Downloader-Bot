from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Translation(object):
    START_TEXT = """Merhaba {},
Ben bir URL Yükleyicisiyim!
Bu Botu kullanarak HTTP/HTTPS bağlantılarını yükleyebilirsiniz!"""
    START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Destek', url='https://t.me/botsohbet'),
        InlineKeyboardButton('Kanal', url='https://t.me/torrentler')
        ],[
        InlineKeyboardButton('Yardım Menüsü', callback_data='help')
        ]]
    )
    HELP_TEXT = """Nasıl kullanılırım? Aşağıdaki adımları izleyin!
    
1. URL gönderin.
2. Kapak fotoğrafı için fotoğraf gönderin. (İsteğe bağlı)
3. Buton seçin.
Bot cevap vermediyse @thebans ile iletişime geçin"""
