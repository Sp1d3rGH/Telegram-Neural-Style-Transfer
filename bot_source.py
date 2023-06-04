import neural_network_source
import telebot
import os
from telebot import  types
from time import sleep
bot = telebot.TeleBot("6135446640:AAHUU00ijGRJsTlO6KfB_GjlAJO6TavGDcg")

@bot.message_handler(commands=['start'])
def start_message(message):
    chatId = message.chat.id
    text = message.text.lower



    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_prom = types.KeyboardButton("/begin")
    item_prom2 = types.KeyboardButton("/info")
    markup2.add(item_prom, item_prom2)
    bot.send_message(chatId, text="Hello, I am a bot that gives your photo the style of a famous painting."
                             " To get the desired result, you will have to follow the instructions to go"
                                  " through 6 simple steps, such as getting started, uploading the image"
                                  " you want to change, confirming the image, uploading the image in the"
                                  " style of which the result will be obtained, choosing the number of"
                                  " iterations and processing your request. Using the /info command, you"
                                  " can get the necessary instructions at any step of interaction with me."
                                  " To get started, use the /begin command.", reply_markup=markup2)

dict1 = {}


@bot.message_handler(commands=['begin'])
def start_begin(message):

    if message.chat.id not in dict1:
        dict1[message.chat.id] = []
        dict1[message.chat.id].append(1)
        bot.send_message(message.chat.id, 'Upload the picture you want to change.')
    else:
        bot.delete_message(message.chat.id, message.id)
        message_prom = bot.send_message(message.chat.id, 'You are still working on creating another picture.'
                                                         ' Please complete the previous steps by clicking on'
                                                         ' the buttons according to your requirements.')
        sleep(5)
        bot.delete_message(message.chat.id, message_prom.id)


@bot.message_handler(commands=['info'])
def start_info(message):
    bot.delete_message(message.chat.id, message.id)
    if message.chat.id not in dict1:
        message_prom = bot.send_message(message.chat.id, 'Use the /begin command to get started.')
        sleep(5)
        bot.delete_message(message.chat.id, message_prom.id)
    elif len(dict1[message.chat.id]) == 1:
        message_prom = bot.send_message(message.chat.id, 'Upload the picture you want to change.')
        sleep(5)
        bot.delete_message(message.chat.id, message_prom.id)
    elif len(dict1[message.chat.id]) == 2 and dict1[message.chat.id][0] == 0:
        message_prom = bot.send_message(message.chat.id, 'Confirm the first image by pressing "Continue", or '
                                                         'press "Stop" to select another.')
        sleep(5)
        bot.delete_message(message.chat.id, message_prom.id)
    elif len(dict1[message.chat.id]) == 2 and dict1[message.chat.id][0] == 1:
        message_prom = bot.send_message(message.chat.id, 'Upload the image the style of which, you want.')
        sleep(5)
        bot.delete_message(message.chat.id, message_prom.id)
    elif len(dict1[message.chat.id]) == 4 and dict1[message.chat.id][0] == 0:
        message_prom = bot.send_message(message.chat.id, 'Choose the number of iterations or stop the process')
        sleep(5)
        bot.delete_message(message.chat.id, message_prom.id)
    elif len(dict1[message.chat.id]) == 5:
        message_prom = bot.send_message(message.chat.id, 'Please wait until I finish processing the result for you.')
        sleep(5)
        bot.delete_message(message.chat.id, message_prom.id)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, "I'm sorry, I don't understand you."
                                          " Please follow the instruction to get the result."
                                          " You can call it with /start.")

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        if message.chat.id in dict1 and dict1[message.chat.id][0] == 1:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            if len(dict1[message.chat.id]) == 1:

                src1 = 'photo1.jpg'
                i = 0
                if not os.path.isfile('photo1.jpg'):
                    with open(src1, 'wb') as new_file:
                        new_file.write(downloaded_file)
                    dict1[message.chat.id].append(src1)

                else:
                    while os.path.isfile(src1):
                        i += 1
                        src1 = 'photo1' + str(i) +'.jpg'
                        if not os.path.isfile(src1):
                            with open(src1, 'wb') as new_file:
                                new_file.write(downloaded_file)

                            dict1[message.chat.id].append(src1)
                            break
                dict1[message.chat.id][0] = 0
                markup = types.InlineKeyboardMarkup(row_width=1)
                item = types.InlineKeyboardButton('Stop', callback_data='stop')
                item1 = types.InlineKeyboardButton('Continue', callback_data='continue')
                markup.add(item, item1)
                bot.send_message(message.chat.id, 'Confirm that the uploaded image is correct.'
                                                  ' If you want to choose another one, click on the Stop button,'
                                                  ' otherwise continue the program by clicking'
                                                  ' the Continue button.', reply_markup=markup)

            elif len(dict1[message.chat.id]) == 2:
                src2 = 'photo2.jpg'
                i = 0
                if not os.path.isfile('photo2.jpg'):
                    with open(src2, 'wb') as new_file:
                        new_file.write(downloaded_file)
                    dict1[message.chat.id].append(src2)

                else:
                    while os.path.isfile(src2):
                        i += 1
                        src2 = 'photo2' + str(i) + '.jpg'
                        if not os.path.isfile(src2):
                            with open(src2, 'wb') as new_file:
                                new_file.write(downloaded_file)
                            dict1[message.chat.id].append(src2)
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

                dict1[message.chat.id][0] = 0
                markup = types.InlineKeyboardMarkup(row_width=1)
                item = types.InlineKeyboardButton('100 iterations', callback_data='100')
                item1 = types.InlineKeyboardButton('500 iterations', callback_data='500')
                item2 = types.InlineKeyboardButton('1000 iterations', callback_data='1000')
                item3 = types.InlineKeyboardButton('Stop', callback_data='stop')
                markup.add(item, item1, item2, item3)
                bot.send_message(message.chat.id, 'Select the number of iterations. The quality'
                                                  ' of the image and the time of its creation will '
                                                  'depend on this. The higher the number of iterations, '
                                                  'the stronger the style transfer will be, but at the same '
                                                  'time the program execution time will also increase. If you '
                                                  'want to change images, press a Stop button.', reply_markup=markup)
        elif message.chat.id not in dict1:
            bot.delete_message(message.chat.id, message.id)
            message_prom = bot.send_message(message.chat.id, "You haven't started working on creating your image yet."
                                                             " You can do this using the /begin command.")

            sleep(5)
            bot.delete_message(message.chat.id, message_prom.id)

        else:
            bot.delete_message(message.chat.id, message.id)
            message_prom =bot.send_message(message.chat.id, 'You are still working on creating another picture.'
                                                         ' Please complete the previous steps by clicking on'
                                                         ' the buttons according to your requirements.')

            sleep(5)
            bot.delete_message(message.chat.id, message_prom.id)
    except Exception as e:
        bot.reply_to(message, e)


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == "continue":
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id,'Great! Now send the second picture.')
            dict1[call.message.chat.id][0] = 1
            return
        if call.data == '100':
            dict1[call.message.chat.id].append(1)
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, 'It may take some time.')
            neural_network_source.start_nst(dict1[call.message.chat.id][1], dict1[call.message.chat.id][2], 100,
                                            dict1[call.message.chat.id][3])
            bot.send_message(call.message.chat.id, "Great, here's your final picture. If you are dissatisfied with it, try "
                                                   "again with a different number of iterations.\nAnd please send me more pictures,"
                                                   " I really love working with them.")
            bot.send_photo(call.message.chat.id, open(dict1[call.message.chat.id][3], 'rb'))
        if call.data == '500':
            dict1[call.message.chat.id].append(1)
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id,'It may take some time.')
            neural_network_source.start_nst(dict1[call.message.chat.id][1], dict1[call.message.chat.id][2], 500,
                                            dict1[call.message.chat.id][3])
            bot.send_message(call.message.chat.id,
                             "Great, here's your final picture. If you are dissatisfied with it, try "
                             "again with a different number of iterations.\nAnd please send me more pictures,"
                             " I really love working with them.")
            bot.send_photo(call.message.chat.id, open(dict1[call.message.chat.id][3], 'rb'))
        if call.data == '1000':
            dict1[call.message.chat.id].append(1)
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, 'It may take some time.')
            neural_network_source.start_nst(dict1[call.message.chat.id][1], dict1[call.message.chat.id][2], 1000,
                                            dict1[call.message.chat.id][3])
            bot.send_message(call.message.chat.id,
                             "Great, here's your final picture. If you are dissatisfied with it, try "
                             "again with a different number of iterations.\nAnd please send me more pictures,"
                             " I really love working with them.")
            bot.send_photo(call.message.chat.id, open(dict1[call.message.chat.id][3], 'rb'))
        if call.data == 'stop':
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id,'Process stopped.')

            if len(dict1[call.message.chat.id]) == 2:
                os.remove(dict1[call.message.chat.id][1])
                del dict1[call.message.chat.id]
                return

        if os.path.isfile(dict1[call.message.chat.id][3]):
            os.remove(dict1[call.message.chat.id][3])
        os.remove(dict1[call.message.chat.id][1])
        os.remove(dict1[call.message.chat.id][2])
        del dict1[call.message.chat.id]

bot.polling()
