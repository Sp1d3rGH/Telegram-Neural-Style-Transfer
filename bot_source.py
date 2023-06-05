import neural_network_source
import telebot
import os
from telebot import  types
from time import sleep
bot = telebot.TeleBot("6135446640:AAHUU00ijGRJsTlO6KfB_GjlAJO6TavGDcg")

dict1 = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    text = message.text.lower

    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_prom = types.KeyboardButton("/begin")
    item_prom2 = types.KeyboardButton("/info")
    markup2.add(item_prom, item_prom2)
    bot.send_message(message.chat.id, text="Welcome to Neural Style Transfer Bot!\n\nEver wanted to apply a style"
                                           " of world-famous artists to your photos? Well, here in just a few steps"
                                           " you can take a look what could happen if someone actually painted your"
                                           " photo!\n\nType '/begin' or click on corresponding button to get started"
                                           " and use '/info' to show hints for ongoing process.", reply_markup=markup2)


@bot.message_handler(commands=['begin'])
def start_begin(message):

    if message.chat.id not in dict1:
        dict1[message.chat.id] = []
        dict1[message.chat.id].append(1)
        bot.send_message(message.chat.id, "Upload the image you want to change.")
    else:
        bot.delete_message(message.chat.id, message.id)
        message_prom = bot.send_message(message.chat.id, "You are still working on creating another picture.\n"
                                                         "Please, follow the steps according to queries.")
        sleep(10)
        bot.delete_message(message.chat.id, message_prom.id)


@bot.message_handler(commands=['info'])
def start_info(message):
    bot.delete_message(message.chat.id, message.id)
    if message.chat.id not in dict1:
        message_prom = bot.send_message(message.chat.id, "Use the '/begin' to get started.")
        sleep(10)
        bot.delete_message(message.chat.id, message_prom.id)
    elif len(dict1[message.chat.id]) == 1:
        message_prom = bot.send_message(message.chat.id, "As suggested, upload the picture you want to change.\n"
                                                         "Make sure your photos are in .png or .jpeg (.jpg) formats"
                                                         " and select 'Compress images' option in Telegram.")
        sleep(10)
        bot.delete_message(message.chat.id, message_prom.id)
    elif len(dict1[message.chat.id]) == 2 and dict1[message.chat.id][0] == 0:
        message_prom = bot.send_message(message.chat.id, "'Continue' - confirm an image and proceed further\n"
                                                         "'Stop' - return to pre-begin stage.")
        sleep(10)
        bot.delete_message(message.chat.id, message_prom.id)
    elif len(dict1[message.chat.id]) == 2 and dict1[message.chat.id][0] == 1:
        message_prom = bot.send_message(message.chat.id, "As suggested, upload the image with desirable art style.\n"
                                                         "Make sure your photos are in .png or .jpeg (.jpg) formats"
                                                         " and select 'Compress images' option in Telegram.")
        sleep(10)
        bot.delete_message(message.chat.id, message_prom.id)
    elif len(dict1[message.chat.id]) == 4 and dict1[message.chat.id][0] == 0:
        message_prom = bot.send_message(message.chat.id, "Choose the number of iterations or stop the process.\n"
                                                         "100 Iterations - weaker affinity.\n"
                                                         "500 Iterations - strong affinity.\n"
                                                         "1000 Iterations - strongest affinity.\n"
                                                         "'Stop' - return to pre-begin stage.")
        sleep(10)
        bot.delete_message(message.chat.id, message_prom.id)
    elif len(dict1[message.chat.id]) == 5:
        message_prom = bot.send_message(message.chat.id, 'Please, wait until I finish processing the result for you.')
        sleep(10)
        bot.delete_message(message.chat.id, message_prom.id)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, "It seems there is no response that could be given to this.\n"
                                          "Check out the introduction message with '/start' to begin.")

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
                bot.send_message(message.chat.id, "Confirm that the uploaded image is correct.\n"
                                                  "If you're unsure, abort the process with 'Stop'"
                                                  " or proceed further with 'Continue'.", reply_markup=markup)

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
                item = types.InlineKeyboardButton('100 Iterations (~10 minutes)', callback_data='100')
                item1 = types.InlineKeyboardButton('500 Iterations (~30 minutes)', callback_data='500')
                item2 = types.InlineKeyboardButton('1000 Iterations (~1 hour)', callback_data='1000')
                item3 = types.InlineKeyboardButton('Stop', callback_data='stop')
                markup.add(item, item1, item2, item3)
                bot.send_message(message.chat.id, "Select the number of iterations.\nThe resemblance of style"
                                                  " to output image shall depend on it, so does the"
                                                  " processing time.", reply_markup=markup)
        elif message.chat.id not in dict1:
            bot.delete_message(message.chat.id, message.id)
            message_prom = bot.send_message(message.chat.id, "You haven't initialized the process yet."
                                                             " Start with '/begin' command.")
            sleep(10)
            bot.delete_message(message.chat.id, message_prom.id)
        else:
            bot.delete_message(message.chat.id, message.id)
            message_prom = bot.send_message(message.chat.id, "You are still working on creating another image.\n"
                                                             "Please, follow the steps according to queries.")
            sleep(10)
            bot.delete_message(message.chat.id, message_prom.id)
    except Exception as e:
        bot.reply_to(message, e)


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == "continue":
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, "Great! Upload the image with desirable art style.")
            dict1[call.message.chat.id][0] = 1
            return
        if call.data == '100':
            dict1[call.message.chat.id].append(1)
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, "Please, wait until your image is processed.")
            neural_network_source.start_nst(dict1[call.message.chat.id][1], dict1[call.message.chat.id][2], 100,
                                            dict1[call.message.chat.id][3])
            bot.send_message(call.message.chat.id, "There is a final result!\nIf you feel so, you can start anew"
                                                   "with '/begin'.")
            bot.send_photo(call.message.chat.id, open(dict1[call.message.chat.id][3], 'rb'))
        if call.data == '500':
            dict1[call.message.chat.id].append(1)
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, "Please, wait until your image is processed.")
            neural_network_source.start_nst(dict1[call.message.chat.id][1], dict1[call.message.chat.id][2], 500,
                                            dict1[call.message.chat.id][3])
            bot.send_message(call.message.chat.id, "There is a final result!\nIf you feel so, you can start anew"
                                                   "with '/begin'.")
            bot.send_photo(call.message.chat.id, open(dict1[call.message.chat.id][3], 'rb'))
        if call.data == '1000':
            dict1[call.message.chat.id].append(1)
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, "Please, wait until your image is processed.")
            neural_network_source.start_nst(dict1[call.message.chat.id][1], dict1[call.message.chat.id][2], 1000,
                                            dict1[call.message.chat.id][3])
            bot.send_message(call.message.chat.id, "There is a final result!\nIf you feel so, you can start anew"
                                                   "with '/begin'.")
            bot.send_photo(call.message.chat.id, open(dict1[call.message.chat.id][3], 'rb'))
        if call.data == 'stop':
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, 'Process aborted.')

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
