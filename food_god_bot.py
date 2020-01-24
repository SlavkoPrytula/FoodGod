import telebot
import time
import os
from emoji import emojize
import random

####################################################################################
bot = telebot.TeleBot("1003017531:AAFvnyEc2kFVU75yyUBp3ZJbGS98VS4HwUA")
#setting the chat_ID:
# chat_ID = bot.get_updates()
# try:
#     chat_ID = chat_ID[0].message.chat.id
# except IndexError:
#     pass
####################################################################################

from urllib.request import urlopen
from bs4 import BeautifulSoup

# user_input = str(input())


import requests
import shutil



# image_url = "https://www.dev2qa.com/demo/images/green_button.jpg"

####################################################################################

# ADD RECIPE:
@bot.message_handler(commands=["recipes"])
def send_my_recipes(message):
    bot.send_message(message.chat.id, "Your delitious recipes")
    with open("{}-recipes.txt".format(message.chat.id)) as f:
        for num, line in enumerate(f.readlines()): 
            print(line)
            my_recipe = emojize(":play_button:", use_aliases=True) + "RECIPE" + emojize(":reverse_button:", use_aliases=True) + "\n\n"
            text = line.split("&")
            print(text)
            bot.send_message(message.chat.id, "{}. {}".format(num+1, text[2]) + "\n\n" + text[3])
            for item in range(len(text[5:-1])):
                my_recipe += emojize(":small_orange_diamond:", use_aliases=True) + text[item+5] + "\n\n"
            bot.send_message(message.chat.id, my_recipe)


####################################################################################
    









chat_id = 0
items = []
added_names = []    
added_id = []
added_videos = []
@bot.message_handler(content_types=['text'])
def handle_messages(message):
    try:
        for i in range(5):
            os.remove("food_{}.jpg".format(i))
    except:
        pass
    
    if str(message.text).lower()[:1] != "/":
        user_input = str(message.text).lower() if len(str(message.text).lower().split()) == 1 else "".join(word + "/" for word in str(message.text).lower().split())

    else:
        pass

    items = []

    URL = 'https://www.allrecipes.com/search/results/{}/'.format(user_input)
    print(URL)
    html = urlopen(URL)

    soup = BeautifulSoup(html, 'html.parser')
    # Get the title
    title = soup.title
    print(title)

    all_links = soup.find_all("a")
    all_images = soup.find_all("img")
    
    count = 0
    chat_id = message.chat.id
    calories = ""
    time_to_cook = ""
    # print(chat_id)\

    

    for link in all_links:
        if count >= 5:
            for item in items:
                get_url = item[3]
                html = urlopen(get_url)
                soup = BeautifulSoup(html, 'html.parser')
                all_food_data = soup.find_all("span")
                for food in all_food_data:
                    calorie_count = food.get("aria-label")
                    if calorie_count != None and "calories" in calorie_count:
                        item.append(calorie_count)
                    if calorie_count != None and "ready" in str(calorie_count).lower():
                        item.append(calorie_count)
            # print(items)
            # print()
            # print(added_names)
            # print()
            # print(added_id)
            for item in range(len(items)):
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.add(telebot.types.InlineKeyboardButton('foodgod', callback_data='get-item-{}-{}'.format(items[item][0], items[item][1])))
                # bot.send_message(message.chat.id, '{}'.format(items[item][2]))
                try:
                    foto = open("food_{}.jpeg".format(item), "rb")
                    bot.send_photo(message.chat.id, foto)
                except:
                    pass
                # bot.send_photo(message.chat.id, "food_{}.jpeg".format(item))
                text = str('{}'.format(items[item][1]) + "\n" + emojize(":fire:", use_aliases=True) + " " + '{}'.format(items[item][-1] if "clories" in str(items[item][-1]) else random.randint(100,500)) + "\n" + emojize(":alarm_clock:", use_aliases=True) + " " + '{}'.format(items[item][-2] if "minutes" in str(items[item][-2]).lower() else "45 Minutes"))
                bot.send_message(message.chat.id, "{}".format(text), reply_markup=keyboard)   #name, calories, time to cook   
                # count += 1Alarm
            break
            
        recipe = link.get("href")
        # print(recipe)
        if recipe != None and user_input in recipe:
            


            name_of_recipe = "".join(word.capitalize() + " " for word in str(recipe).split('/')[-2].split('-'))
            item = [str(recipe).split('/')[-3], name_of_recipe]
            if item[1] not in added_names or item[0] not in added_id:
                # print(added_names)
                # print(item[1] not in added_names,"__________", item[1])
                # print(added)
                for image in all_images:
                    name = image.get("title")
                    img = image.get("data-original-src")
                    type_of_data = str(recipe).split('/')[3]   #recipe/video...
                    # print(type_of_data)
                    if name != None and name_of_recipe in name and type_of_data == "recipe" and count < 5 and name not in added_videos:
                        # print(name,"--------",item[1])
                        # print(name_of_recipe)
                        # print(type_of_data)
                        # print(img)
                        # print()
                        item.append(img)
                        resp = requests.get(img, stream=True)
                        local_file = open('food_{}.jpeg'.format(count), 'wb')
                        resp.raw.decode_content = True
                        shutil.copyfileobj(resp.raw, local_file)
                        del resp
                        item.append(recipe)
                        
                            
                        added_videos.append(name)
                        items.append(item)
                        added_names.append(item[1])
                        added_id.append(item[0])
                        count += 1

            

    


    # for image in all_images:
    #     img = image.get("src")
    #     print(img)


        

# all_links = soup.find_all("label")
# for link in all_links:
#     recipe = link.get("title")
#     if recipe != None:
#         print(recipe)



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text='CLick me', callback_data='add')
    markup.add(button)
    bot.reply_to(message, "Howdy, how are you doing?")



from telebot import types
# @bot.message_handler(commands=['test'])
# def send_welcom(message):
#     markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
#     markup.add('1', '2') #Имена кнопок
#     msg = bot.reply_to(message, 'Test text', reply_markup=markup)
#     bot.register_next_step_handler(msg, callback=None)


# @bot.message_handler(commands=['test'])
# def get_items(message):
#     for item in items:
#         keyboard = telebot.types.InlineKeyboardMarkup()
#         keyboard.add(telebot.types.InlineKeyboardButton('foodgod', callback_data='get-item-{}'.format(item[0])))
#         bot.send_message(message.chat.id, '{}'.format(item[1]), reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global get_the_video
    saved_items = []
    liked_items_num = {}
    try:
        with open("{}-recipes.txt".format(query.from_user.id), "r") as f:
            for line in f.readlines():
                item_id = line.split("&")[2]
                saved_items.append(item_id)
        f.close()
    except:
        with open("{}-recipes.txt".format(query.from_user.id), "w") as f:
            f.write("")


    if "get" in str(query):
        print(query.from_user.id)
        data = "".join(str(item.replace(" ", "-")).lower() + "/" for item in str(query.data).split("-")[2:4])
        print(data, "-data")

        URL = 'https://www.allrecipes.com/recipe/{}'.format(data)
        print(URL)
        html = urlopen(URL)
        soup = BeautifulSoup(html, 'html.parser')

        ingredients = []
        all_ingredients = soup.find_all("label")
        for ingredient in all_ingredients:
            ing = ingredient.get("title")
            print(ing)
            if ing != None:
                ingredients.append(ing)
        print(ingredients)

        videos = []
        all_videos = soup.find_all("a")


        for video in all_videos:

            vid = video.get("href")
            try:
                type_of_data = str(vid).split('/')[3]   #recipe/video...
                # print(vid)
                if vid != None and type_of_data == 'video':
                    videos.append(vid)
            except:
                pass

        print(videos)
        # bot.send_message(query.from_user.id, videos[0])

        get_youtube_text = str(data).split("/")[-2].replace("-", "+")
        get_youtube_text = get_youtube_text[0:len(get_youtube_text)-1] + "+" + "allrecipes"
        youtube_url = "https://www.youtube.com/results?search_query={}".format(get_youtube_text)
        print(youtube_url)

        html = urlopen(youtube_url)
        soup = BeautifulSoup(html, 'html.parser')

        links = []
        all_videos = soup.find_all("a")
        try:
            try:
                for video in all_videos:
                    name = video.get("title")
                    if name != None and "| Allrecipes.com" in name:
                        link = video.get("href")
                        links.append(link)

                print(links)
                get_the_video = "https://www.youtube.com" + links[0]
                # bot.send_message(query.from_user.id, emojize(":play_button:", use_aliases=True) + "RECIPE" + emojize(":reverse_button:", use_aliases=True) + "\n\n")
                text = emojize(":tv:", use_aliases=True) + "  " + "Watch a video: " + "\n" + get_the_video
                bot.send_message(query.from_user.id, text)
            except:
                food_name = "".join(str(word).capitalize() + " " for word in (data.split("/")[-2]).split("-"))
                # print()
                # print(food_name)
                # print()
                for video in all_videos:
                    name = video.get("title")
                    # print(name)
                    # print(name)
                    if name != None:
                        for word in food_name.split():
                            if word in name:    
                                # print(name, "- name")
                                link = video.get("href")
                                links.append(link)

                print(links)
                get_the_video = "https://www.youtube.com" + links[0]
                # bot.send_message(query.from_user.id, emojize(":play_button:", use_aliases=True) + "RECIPE" + emojize(":reverse_button:", use_aliases=True) + "\n\n")
                text = emojize(":tv:", use_aliases=True) + "  " + "Watch a video: " + "\n\n" + get_the_video
                bot.send_message(query.from_user.id, text)

        except:
            print('oops...')
            bot.send_message(query.from_user.id, "Hmmm... It seems like no video was found" + emojize(":frowning_face:", use_aliases=True))




        text = emojize(":play_button:", use_aliases=True) + "RECIPE" + emojize(":reverse_button:", use_aliases=True) + "\n\n"

        global recipe_text
        recipe_text = "".join(word + "&" for word in ingredients)
        print(recipe_text)

        new_items = ""
        for item in range(len(ingredients)):
            first_item = ingredients[item][:1]
            if first_item.isdigit():
                text += emojize(":small_orange_diamond:", use_aliases=True)+ "     " + ingredients[item] + "\n\n"
                new_items += ingredients[item] + "-"
            else:
                text += ingredients[item] + "\n\n\n"
        print(text)
        
        item_id = str(query.data).split("-")[2] + "-" + str(query.data).split("-")[3]
        print(item_id, "--------------------------------------------111111111111111111111111111111111")
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton('Save to my recipes', callback_data='save-item-{}'.format(item_id)))
        # recipe_text = 
        
        print(chat_id)
        bot.send_message(query.from_user.id, text, reply_markup=keyboard)
        # bot.send_message(chat_ID, text)
        # bot.send_message(chat_ID, " "*10+text)
    
    if "save" in str(query):
        # print(query.data)
        # print("here")
        # print(recipe_text)
        # print(get_the_video)

        try:
            topic = "1"
            user_id = query.from_user.id 
            item_ID = str(query.data).split("-")[2] + "&" + str(query.data).split("-")[3]
            # print(recipe_text)
            
            with open("{}-recipes.txt".format(user_id), "a") as f: #w - overwrites a - extends text
                if item_ID.split("&")[1] not in saved_items:
                    print()
                    print(item_ID)
                    print(saved_items)
                    print()
                    f.write(topic + "&" + item_ID + "&" + get_the_video + "&" + "&" + recipe_text + "\n")
            f.close()
        except:
            bot.send_message(user_id, "Can't import recipe...")

       

	




while True:
    try:
        bot.polling()
    except:
        time.sleep(15)

