import neural_network_source
import telebot
import os

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

            neural_network_source.start_nst(dict1[message.chat.id][0], dict1[message.chat.id][1], 1, dict1[message.chat.id][2])
            bot.send_photo(message.chat.id, open(dict1[message.chat.id][2], 'rb'))
            os.remove(dict1[message.chat.id][2])
            os.remove(dict1[message.chat.id][0])
            os.remove(dict1[message.chat.id][1])
            del dict1[message.chat.id]


    except Exception as e:
        bot.reply_to(message, e)


bot.polling()