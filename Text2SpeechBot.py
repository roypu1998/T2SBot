from telebot import TeleBot
from googletrans import Translator, constants
import speech_recognition as sr
from gtts import gTTS
import os


Token="1440147560:AAEPQcO5676me59Eix1R7xMG1Hd9ka_Wazc"
bot=TeleBot(Token)

#When user sends 'start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id,"typing")
    bot.send_message(message.chat.id,"Enter text to bot make it a message voice")


#When user sends any text except from 'start'
@bot.message_handler(func=lambda msg: True)
def send_voice_msg(msg):
    if os.path.exists('speak.mp3'):
        os.remove('speak.mp3')


    translator = Translator()
    text=msg.text
    translation = translator.translate(text=text, dest='en')
    #print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")

    speech = msg.text
    if speech != translation.text:
        speech = translation.text


    language = 'en'
    myobj = gTTS(text=speech, lang=language, slow=False)
    # Saving the converted audio in a mp3 file named
    # welcome
    myobj.save("speak.mp3")

    if speech == "Done" or speech == "Done.lower" or speech == "Bye":
        bot.send_chat_action(msg.chat.id, "typing")
        bot.send_message(msg.chat.id, "Enter text to bot make it a message voice")
    else:
        bot.send_voice(msg.chat.id,voice=open('speak.mp3', 'rb'),reply_to_message_id=msg.message_id )
        bot.send_message(msg.chat.id,f'{translation.text}')

    if os.path.exists('speak.mp3'):
        os.remove('speak.mp3')



#When user sends any voice message
@bot.message_handler(content_types=['voice'])
def handle_voiceMsg(voiceMsg):

    if os.path.exists('voice.wav'):
        os.remove('voice.wav')

    file_info = bot.get_file(voiceMsg.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('voice.wav', 'wb') as voiceMessage:
        voiceMessage.write(downloaded_file)

    print('saving file...')
    r = sr.Recognizer()

    print('recored....')
    voice=sr.AudioFile('voice.wav')

    print("open wav file....")
    with voice as source:
        audio_text = r.listen(source)

    try:
        print("try....")
        text = r.recognize_google(audio_text)
        bot.send_chat_action(voiceMsg.chat.id, "typing")
        bot.send_message(voiceMsg.chat.id, text=text, reply_to_message_id=voiceMsg.message_id)
        print('Successfully!')

    except:
        print('unSuccessfully...')
        bot.send_chat_action(voiceMsg.chat.id, "typing")
        bot.send_message(voiceMsg.chat.id,"Sorry, Try again...",reply_to_message_id=voiceMsg.message_id)

bot.polling()