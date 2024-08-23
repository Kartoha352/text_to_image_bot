import telebot
import config

from logic import Text2ImageAPI

API_TOKEN = config.TOKEN

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Напиши мне prompt, чтобы я отправил сгенерированную картинку в чат.")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    prompt = message.text

    api_url = "https://api-key.fusionbrain.ai/"
    api_key = config.API_TOKEN
    secret_key = config.SECRET_KEY

    api = Text2ImageAPI(api_url, api_key, secret_key)
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid)[0]
    
    api.save_image(images, "decoded_image.jpg")

    with open('decoded_image.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


bot.infinity_polling()