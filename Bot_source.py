import neural_network_source
import telebot
import os
from telebot import  types
bot = telebot.TeleBot("6135446640:AAHUU00ijGRJsTlO6KfB_GjlAJO6TavGDcg")

@bot.message_handler(commands=['start'])
def start_message(message):
    chatId = message.chat.id
    text = message.text.lower

    bot.send_message(chatId, "Hello, I am a bot that gives your photo the style of a famous painting."
                             " To get the result, please send separate messages first to the photo you want to change,"
                             " and then to the picture in the style of which you need to get the photo.")


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, "I'm sorry, I don't understand you."
                                          " Please follow the instruction to get the result."
                                          " You can call it with /start.")


dict1 = {}



@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        if message.chat.id not in dict1:

            dict1[message.chat.id] =[]

            src1 = 'photo1.jpg'
            i = 0
            if not os.path.isfile('photo1.jpg'):
                with open(src1, 'wb') as new_file:
                    new_file.write(downloaded_file)
                dict1[message.chat.id].append(src1)
                bot.send_message(message.chat.id, "Great! Now send the second picture.")

            else:
                while os.path.isfile(src1):
                    i += 1
                    src1 = 'photo1' + str(i) +'.jpg'
                    if not os.path.isfile(src1):
                        with open(src1, 'wb') as new_file:
                            new_file.write(downloaded_file)

                        dict1[message.chat.id].append(src1)
                        bot.send_message(message.chat.id, "Great! Now send the second picture.")
                        break

            markup = types.InlineKeyboardMarkup(row_width=1)
            item = types.InlineKeyboardButton('stop', callback_data='stop')
            item1 = types.InlineKeyboardButton('continue', callback_data='continue')
            markup.add(item, item1)
            bot.send_message(message.chat.id, 'дарова1', reply_markup=markup)

        elif message.chat.id in dict1:
            src2 = 'photo2.jpg'
            i = 0
            if not os.path.isfile('photo2.jpg'):
                with open(src2, 'wb') as new_file:
                    new_file.write(downloaded_file)
                dict1[message.chat.id].append(src2)
                bot.send_message(message.chat.id, "It may take some time.")

            else:
                while os.path.isfile(src2):
                    i += 1
                    src2 = 'photo2' + str(i) + '.jpg'
                    if not os.path.isfile(src2):
                        with open(src2, 'wb') as new_file:
                            new_file.write(downloaded_file)
                        dict1[message.chat.id].append(src2)
                        bot.send_message(message.chat.id, "It may take some time.")
                        break


            src3 = 'photo3.jpg'
            j = 0
            if not os.path.isfile('photo3.jpg'):
                dict1[message.chat.id].append(src3)
            else:
                while os.path.isfile(src3):
                    j += 1
                    src3 = 'photo3' + str(j) + '.jpg'
                    if not os.path.isfile(src3):
                        dict1[message.chat.id].append(src3)
                        break




            markup = types.InlineKeyboardMarkup(row_width=1)
            item = types.InlineKeyboardButton('100', callback_data='100')
            item1 = types.InlineKeyboardButton('500', callback_data='500')
            item2 = types.InlineKeyboardButton('1000', callback_data='1000')
            item3 = types.InlineKeyboardButton('stop', callback_data='stop')
            markup.add(item, item1, item2, item3)
            bot.send_message(message.chat.id, 'дарова', reply_markup=markup)


    except Exception as e:
        bot.reply_to(message, e)


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == "continue":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Great! Now send the second picture.')
            return
        if call.data == '100':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='иди нахуй')
            neural_network_source.start_nst(dict1[call.message.chat.id][0], dict1[call.message.chat.id][1], 1,
                                            dict1[call.message.chat.id][2])

            bot.send_photo(call.message.chat.id, open(dict1[call.message.chat.id][2], 'rb'))
        if call.data == '500':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='иди нахуй')
            neural_network_source.start_nst(dict1[call.message.chat.id][0], dict1[call.message.chat.id][1], 10,
                                            dict1[call.message.chat.id][2])

            bot.send_photo(call.message.chat.id, open(dict1[call.message.chat.id][2], 'rb'))
        if call.data == '1000':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='иди нахуй')
            neural_network_source.start_nst(dict1[call.message.chat.id][0], dict1[call.message.chat.id][1], 15,
                                            dict1[call.message.chat.id][2])

            bot.send_photo(call.message.chat.id, open(dict1[call.message.chat.id][2], 'rb'))
        if call.data == 'stop':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='stopped')

            if len(dict1[call.message.chat.id]) == 1:
                os.remove(dict1[call.message.chat.id][0])
                del dict1[call.message.chat.id]
                return

        if os.path.isfile(dict1[call.message.chat.id][2]):
            os.remove(dict1[call.message.chat.id][2])
        os.remove(dict1[call.message.chat.id][0])
        os.remove(dict1[call.message.chat.id][1])
        del dict1[call.message.chat.id]





bot.polling()