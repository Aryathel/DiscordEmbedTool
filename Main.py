import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import requests
import json
from urllib.request import urlopen, HTTPError
import discord
from discord.ext import commands
import datetime

help_embed_image = "HelpEmbed1.PNG"
help_markdown_image = "HelpMarkdown.PNG"

save_file = "./save_data.json"

mode_options = [
    'Webhook',
    'Bot'
]

if os.path.isfile(save_file):
    with open(save_file, "r") as file:
        try:
            save_data = json.loads(file.read())
        except:
            save_data = {}
else:
    save_data = {}
#print(json.dumps(save_data, indent = 4))

def run_setup(data):
    global old_mode
    for entry in data.keys():
        if entry == "mode":
            old_mode = data[entry]
            if data[entry] == "Webhook":
                mode.set(mode_options[0])
                for item in data['Webhook']:
                    if item == "web_or_key":
                        web_or_key.delete(0, tk.END)
                        web_or_key.insert(0, data['Webhook'][item])
                    elif item == "name_or_channel_id":
                        name_or_channel_id.delete(0, tk.END)
                        name_or_channel_id.insert(0, data['Webhook'][item])
            elif data[entry] == "Bot":
                mode.set(mode_options[1])
                for item in data['Bot']:
                    if item == "web_or_key":
                        web_or_key.delete(0, tk.END)
                        web_or_key.insert(0, data['Bot'][item])
                    elif item == "name_or_channel_id":
                        name_or_channel_id.delete(0, tk.END)
                        name_or_channel_id.insert(0, data['Bot'][item])

def save_embed(*event):
    print("Save Embed.")

def load_embed(*event):
    print("Load Embed.")

def show_embeds_help(*event):
    print("Show Embed.")
    show_embed_help = tk.Toplevel(master = root)
    show_embed_help.title("Embedded Message Help")
    show_embed_help.iconbitmap('./icon.ico')
    image = tk.Label(master = show_embed_help, image = emb_img)
    image.pack()

def show_markdown_help(*event):
    print("Show Markdown.")
    show_markdown = tk.Toplevel(master = root)
    show_markdown.title("Discord Markdown Help")
    show_markdown.iconbitmap('./icon.ico')
    image = tk.Label(master = show_markdown, image = mark_img)
    image.pack()

def update_mode(*args):
    global old_mode
    if mode.get() == "Webhook":
        label.config(text = "Enter a Webhook:")
        label2.config(text = "Enter a Name for the Webhook:")
        print(old_mode)
        print(save_data.keys())
        if not old_mode in save_data.keys():
            save_data[old_mode] = {}
        print(json.dumps(save_data, indent = 4))
        save_data[old_mode] = {
            "web_or_key": web_or_key.get(),
            "name_or_channel_id": name_or_channel_id.get()
        }
        print(json.dumps(save_data, indent = 4))
        if "Webhook" in save_data.keys():
            for item in save_data['Webhook']:
                if item == "web_or_key":
                    web_or_key.delete(0, tk.END)
                    web_or_key.insert(0, save_data['Webhook'][item])
                elif item == "name_or_channel_id":
                    name_or_channel_id.delete(0, tk.END)
                    name_or_channel_id.insert(0, save_data['Webhook'][item])
        with open(save_file, 'w') as file:
            file.write(json.dumps(save_data, indent = 4))
        old_mode = "Webhook"
    elif mode.get() == "Bot":
        label.config(text = "Enter a Bot Token:")
        label2.config(text = "Enter a Channel ID To Send To:")
        if not old_mode in save_data.keys():
            save_data[old_mode] = {}
        save_data[old_mode] = {
            "web_or_key": web_or_key.get(),
            "name_or_channel_id": name_or_channel_id.get()
        }
        if "Bot" in save_data.keys():
            for item in save_data['Bot']:
                if item == "web_or_key":
                    web_or_key.delete(0, tk.END)
                    web_or_key.insert(0, save_data['Bot'][item])
                elif item == "name_or_channel_id":
                    name_or_channel_id.delete(0, tk.END)
                    name_or_channel_id.insert(0, save_data['Bot'][item])
        with open(save_file, 'w') as file:
            file.write(json.dumps(save_data, indent = 4))
        old_mode = "Bot"

def send_test():
    if mode.get() == "Webhook":
        try:
            urlopen(web_or_key.get())
            failed = False
        except HTTPError as e:
            if e.msg == "Forbidden":
                failed = False
            else:
                failed = True
        except:
            failed = True
            messagebox.showerror("Failed", "The provided webhook is invalid, please double check the link.")

        if not failed:
            data = {}
            data['content'] = "Just running some tests for a thing, don't mind me."
            data['username'] = name_or_channel_id.get()

            data['embeds'] = []
            embed = {}
            embed['title'] = "Testing title"
            embed['description'] = "tesing the description"
            embed['fields'] = []
            embed['fields'].append({"name": "test", "value":"asd"})
            data['embeds'].append(embed)

            result = requests.post(web_or_key.get(), data = json.dumps(data), headers = {"Content-Type": "application/json"})

            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                print("Delivered message successfully, code {}.".format(result.status_code))
    elif mode.get() == "Bot":
        bot = commands.AutoShardedBot(command_prefix="!", description="Heroicos_HM's Twitter Success Poster", case_insensitive = True)
        bot.remove_command('help')

        bot.TOKEN = web_or_key.get()

        @bot.event
        async def on_ready():
            content = "Don't mind me..still."
            embed = discord.Embed(
                title = "Test title",
                description = "testing description"
            )
            embed.add_field(
                name = "test",
                value = "qwe"
            )
            channel = bot.get_channel(int(name_or_channel_id.get()))
            await channel.send(content = content, embed = embed)
            bot.close()

        bot.run(bot.TOKEN, bot = True, reconnect = False)


def on_closing():
    save_data['mode'] = mode.get()
    if mode.get() == "Webhook":
        save_data['Webhook'] = {
            "web_or_key": web_or_key.get(),
            "name_or_channel_id": name_or_channel_id.get()
        }
    elif mode.get() == "Bot":
        save_data['Bot'] = {
            "web_or_key": web_or_key.get(),
            "name_or_channel_id": name_or_channel_id.get()
        }
    with open(save_file, 'w') as file:
        file.write(json.dumps(save_data, indent = 4))
    root.destroy()

root = tk.Tk()
root.iconbitmap('./icon.ico')
root.tk_setPalette(background='#36393f', foreground='white')
emb_img = ImageTk.PhotoImage(Image.open(os.path.abspath(help_embed_image)))
mark_img = ImageTk.PhotoImage(Image.open(os.path.abspath(help_markdown_image)))
menu = tk.Menu(root, background = '#2b2c31')
root.config(menu = menu, bg = '#36393f')
embed_menu = tk.Menu(menu, bg = '#2b2c31')
help_menu = tk.Menu(menu, bg = '#2b2c31')
menu.add_cascade(label = "File", menu = embed_menu)
menu.add_cascade(label = "Help", menu = help_menu)
embed_menu.add_command(label = "Save", command = save_embed, accelerator = "Ctrl+S")
root.bind("<Control-s>", save_embed)
embed_menu.add_command(label = "Load", command = load_embed, accelerator = "Ctrl+L")
root.bind("<Control-l>", load_embed)
help_menu.add_command(label = "Embeds", command = show_embeds_help, accelerator = "Ctrl+E")
root.bind("<Control-e>", show_embeds_help)
help_menu.add_command(label = "Markdown", command = show_markdown_help, accelerator = "Ctrl+M")
root.bind("<Control-m>", show_markdown_help)

root.title("Hero's Embed Tool")

label3 = tk.Label(master = root, text = "Select Webhook or Bot Mode")
label3.grid(row = 0, column = 0, padx = 5, pady = 2)

label = tk.Label(master = root, text = "Enter a Webhook:")
label.grid(row = 2, column = 0, padx = 5, pady = 2)

label2 = tk.Label(master = root, text = "Enter a Name for the Webhook:")
label2.grid(row = 4, column = 0, pady = 2, padx = 5)

web_or_key = tk.Entry(master = root, width = 50, bg = '#484c52', fg = '#b8babc')
web_or_key.grid(row = 3, column = 0, padx = 5, pady = 2)

test = tk.Button(master = root, width = 25, height = 1, text = "Send Test Embed", command = send_test, bg = '#2b2c31')
test.grid(row = 100, column = 0, padx = 5, pady = 2)

name_or_channel_id = tk.Entry(master = root, width = 50, bg = '#484c52', fg = '#b8babc')
name_or_channel_id.grid(row = 5, column = 0, padx = 5, pady = 2)

mode = tk.StringVar(master = root)

old_mode = "Webhook"
mode.set(mode_options[0])
run_setup(save_data)

mode.trace("w", update_mode)
mode_select = tk.OptionMenu(root, mode, *mode_options)
mode_select.config(width = 20, bg = '#2b2c31')
mode_select.grid(row = 1, column = 0, padx = 5, pady = 2)

root.protocol("WM_DELETE_WINDOW", on_closing)

#run_setup(save_data)

root.mainloop()
