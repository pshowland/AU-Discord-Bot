#! /usr/bin/python3
import discord, os, requests, shutil, math
from PIL import Image, ImageDraw

TOKEN = os.environ.get('AUBOT_TOKEN')

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if(message.content == "!aubot"):
        return_message = "Hello! I'm AU Bot, and I hope to be actually useful!"
        await client.send_message(message.channel, return_message)

    if(message.content == "!roles"):
        server_roles = []
        for role in message.server.roles:
            if(role.name != "@everyone"):
                server_roles.append(role.name)
        return_message = ""
        if(len(server_roles) == 0):
            return_message = "There are currently no roles set on this server!"
        else:
            return_message = "The current roles for this server are: " + str(server_roles)
        await client.send_message(message.channel, return_message)

    if(message.content.find("!roll ") == 0):
        params = message.content[6:]
        n = int(params.split("d")[0])
        d = int(params.split("d")[1])
        if(not math.isnan(d) and not math.isnan(n) and n>0 and d>0):
            mylist = []
            sum = 0
            for i in range(0,n):
                rng = random.randint(1,d)
                mylist.append(rng)
                sum = sum + rng
            msg = message.author.mention+' rolled ' + str(mylist) + '. Total is ' + str(sum)
            await client.send_message(message.channel, msg)

    if(message.content == "!pixel"):
        if(len(message.attachments) != 0):
            file = message.attachments[0]
            r = requests.get(file["url"], stream=True, headers={'User-agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                with open(os.environ.get("WORKING_PATH")+"pixel/"+file["filename"], 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

        im = Image.open(os.environ.get("WORKING_PATH")+"pixel/"+file["filename"])
        output_size = 16
        pps = -1
        width = im.size[0]
        height = im.size[1]
        if(width > 1080 or height > 1080):
            msg = "Image is too large! Please try a smaller image."
            await client.send_message(message.channel, msg)
            return
        if(width > height):
            pps = math.ceil(width/output_size)
        else:
            pps = math.ceil(height/output_size)
        data = list(im.getdata())
        im_arr = []
        for i in range(0,len(data),width):
            im_arr.append(data[i:i+width])
        temp_pixel_avg = (0,0,0)
        out_arr = []
        for j in range(0,height,pps):
            for i in range(0,width,pps):
               for y in range(j,j+pps):
                    for x in range(i,i+pps):
                        try:
                            temp0 = temp_pixel_avg[0] + im_arr[y][x][0]
                            temp1 = temp_pixel_avg[1] + im_arr[y][x][1]
                            temp2 = temp_pixel_avg[2] + im_arr[y][x][2]
                            temp_pixel_avg = (temp0,temp1,temp2)
                        except:
                            pass
               avg0 = int(temp_pixel_avg[0]/(pps**2))
               avg1 = int(temp_pixel_avg[1]/(pps**2))
               avg2 = int(temp_pixel_avg[2]/(pps**2))
               temp_pixel_avg = (avg0,avg1,avg2)
               out_arr.append(temp_pixel_avg)
        square_im_arr = []
        for i in range(0,len(out_arr),output_size):
            square_im_arr.append(out_arr[i:i+output_size])
        new_im = Image.new('RGB',(len(square_im_arr[0]),len(square_im_arr)))
        draw = ImageDraw.Draw(new_im)
        for x in range(0,len(square_im_arr[0])):
            for y in range(0,len(square_im_arr)):
                try:
                    draw.point((x,y),fill=square_im_arr[y][x])
                except:
                    pass
        new_im.save(os.environ.get("WORKING_PATH")+"pixel/"+file["filename"].split(".")[0]+"_icon."+file["filename"].split(".")[1])
        await client.send_file(message.channel, os.environ.get("WORKING_PATH")+"pixel/"+file["filename"].split(".")[0]+"_icon."+file["filename"].split(".")[1])
        os.remove(os.environ.get("WORKING_PATH")+"pixel/"+file["filename"])
        os.remove(os.environ.get("WORKING_PATH")+"pixel/"+file["filename"].split(".")[0]+"_icon."+file["filename"].split(".")[1])

client.run(TOKEN)
