import discord
import responses
import random
byteImg = ''

import urllib.request
from PIL import Image
from io import BytesIO
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps

import moviepy
from moviepy.editor import VideoFileClip

vocabulario = []
emojis = ['😀', '😊', '👍', '👎', '❌', '✔️', '🆗', '🚮', '🔥', '🥵', '😎', '🤡']

async def send_message(username, message, user_message, is_private):
    try:
        response = responses.handle_response(username, user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def image_impact(imagen, command, image_text, gif):

    if not gif:
        imagen.save('cache.png')
    if image_text == 'random':
        image_text = vocabulario[random.randint(0, len(vocabulario) - 1)]

    fontsize = 1
    font = ImageFont.truetype('impact.ttf', size=fontsize)
    w, h = imagen.size
    area = w*h
    print(area)

    print(area)
    if len(image_text) > 10:
        while font.getsize(image_text)[0] < imagen.size[0] * 0.9:
            fontsize += 1
            font = ImageFont.truetype("impact.ttf", fontsize)

        fontsize -= 2
        font = ImageFont.truetype("impact.ttf", fontsize)
    else:
        fontsize = int(round((int(w) * 0.1 / (len(image_text) / len(image_text)))))

    font = ImageFont.truetype("impact.ttf", fontsize)

    textw = font.getsize(image_text)[0]
    texth = font.getsize(image_text)[1]
    fill_color = (255, 255, 255)
    stroke_color = (0, 0, 0)

    d = ImageDraw.Draw(imagen)
    print(command)
    if 'bottom' in command:
        print('bottomtext')
        d.text((w / 2 - textw / 2, h - texth * 1.4), str(image_text), font=font, fill=fill_color, stroke_width= round((4*(area/200000))),
               stroke_fill=stroke_color)
    else:
        d.text((w / 2 - textw / 2, 0), str(image_text), font=font, fill=fill_color, stroke_width=4,
               stroke_fill=stroke_color)

    if gif:
        imagen.save('test.gif')
    else:
        imagen.save('result.png')



def run_discord_bot():
    TOKEN = ''
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        if 'rotom' in user_message and 'opinas' in user_message or 'rotom' in user_message and 'parece' in user_message:
            await message.add_reaction(emojis[random.randint(0,11)])


        elif '/image' in user_message:
            if not '/imagen' in user_message:
                user_message.replace('/image', '/imagen')
            try:
                imagen_url = (message.attachments[0])
                print(imagen_url)
                req = urllib.request.Request(imagen_url, headers={'user-agent': 'velutina'})
                with urllib.request.urlopen(req) as enlace:
                    byteImg = BytesIO(enlace.read())
            except Exception:
                pass

            try:
                my_image = Image.open(byteImg)
            except UnboundLocalError:
                my_image = Image.open('result.png')

            if 'text' in user_message:

                if ';' in  user_message:

                    user_message = user_message.replace('/imagen ', '')
                    user_message = user_message.split('; ')

                    for index in user_message:
                        image_text = index.split('=')[1]
                        image_command = index.split('=')[0]
                        image_impact(my_image, image_command, image_text, False)

                    await message.channel.send(file=discord.File("result.png"))


                else:

                    user_message = user_message.replace('/imagen ', '')
                    user_message = user_message.split('=')
                    image_impact(my_image, user_message[0], user_message[1],False)
                    await message.channel.send(file=discord.File("result.png"))


            elif 'deshacer' in user_message:
                print('deshacer')
                cache = Image.open('cache.png')
                cache.save('result.png')
                await message.channel.send(file=discord.File("cache.png"))


            elif 'png' in user_message:
                my_image.save('result.png', "PNG")
                await message.channel.send(file=discord.File("result.png"))


            elif 'JPEG' in user_message or 'jpeg' in user_message:
                rgb_image = my_image.convert('RGB')
                rgb_image.save('result.jpeg', "JPEG")
                await message.channel.send(file=discord.File("result.jpeg"))


            else:
                await message.channel.send(file=discord.File("result.png"))


        elif '/gif' in user_message:
            try:
                video_url = (message.attachments[0])
                print(video_url)
                my_video = VideoFileClip(str(video_url))
                my_video.write_gif("test.gif")
            except Exception as E:
                my_video = VideoFileClip("test.gif")


            if 'text' in user_message:
                my_video = Image.open('test.gif')
                if ';' in  user_message:

                    user_message = user_message.replace('/gif ', '')
                    user_message = user_message.split('; ')

                    for index in user_message:
                        image_text = index.split('=')[1]
                        image_command = index.split('=')[0]
                        image_impact(my_video, image_command, image_text, True)



                else:

                    user_message = user_message.replace('/gif ', '')
                    user_message = user_message.split('=')
                    image_impact(my_video, user_message[0], user_message[1], True)

            await message.channel.send(file=discord.File("test.gif"))

        else:
            await send_message(username, message, user_message, is_private=False)





    client.run(TOKEN)