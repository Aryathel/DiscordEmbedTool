import tkinter as tk
from PIL import ImageTk, Image
import os
import requests
import json

help_embed_image = "HelpEmbed1.PNG"
help_markdown_image = "HelpMarkdown.PNG"

mode_options = [
    'Webhook',
    'Bot'
]

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
    if mode.get() == "Webhook":
        label.config(text = "Enter a Webhook:")
    elif mode.get() == "Bot":
        label.config(text = "Enter a Bot Token:")

def send_test():
    data = {}
    data['content'] = "Just running some tests for a thing, don't mind me."
    data['username'] = "Heroicos_HM (Webhook Ver.)"

    data['embeds'] = []
    embed = {}
    embed['title'] = "Testing title"
    embed['description'] = "tesing the description"
    embed['fields'] = []
    embed['fields'].append({"name": "test"})
    data['embeds'].append(embed)

    result = requests.post(web_or_key.get(), data = json.dumps(data), headers = {"Content-Type": "application/json"})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Delivered message successfully, code {}.".format(result.status_code))

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

mode = tk.StringVar(master = root)
mode.trace("w", update_mode)
mode.set(mode_options[0])
mode_select = tk.OptionMenu(root, mode, *mode_options)
mode_select.config(width = 20, bg = '#2b2c31')
mode_select.grid(row = 1, column = 0, padx = 5, pady = 2)


web_or_key = tk.Entry(master = root, width = 50, bg = '#484c52', fg = '#b8babc')
web_or_key.grid(row = 3, column = 0, padx = 5, pady = 2)

test = tk.Button(master = root, width = 25, height = 1, text = "Send Test Embed", command = send_test, bg = '#2b2c31')
test.grid(row = 4, column = 0, padx = 5, pady = 2)

label2 = tk.Label(master = root, text = "Enter a title for the embedded message.")

root.mainloop()
