from javascript import require

mineflayer = require('mineflayer')
import tkinter as tk
import time

# import os
# import sys


# Enter the server information here
host = 'localhost'  # Your server address
port = 25550  # Your server port
username = 'ChatBot'  # This can't be changed

bot = mineflayer.createBot({
    'host': host,
    'port': port,
    'username': username
})


def handle_kicked(bot, reason, loggedIn):
    print(f"Kicked from server: {reason}")
    messages_listbox.insert(tk.END, f"Kicked from server: {reason}")
    bot.clearControlStates()
    bot.chat("Connecting to the server...")
    time.sleep(5)
    reconnect_to_server()
    # restart_program()


def reconnect_to_server():
    global bot
    bot = mineflayer.createBot({
        'host': host,
        'port': port,
        'username': username
    })
    bot.chat("Connected")


# def restart_program(bot):
#     python = sys.executable
#     os.execl(python, python, *sys.argv)
#     time.sleep(5)
#     bot.chat("Connected")


bot.on('kicked', handle_kicked)


async def handle_respawn(self):
    # wait for the death screen to appear
    await self.bot.waitFor('death')
    # respawn
    self.bot.respawn()
    time.sleep(1)
    bot.chat('Respawned')


def handle_chat(this, username, message, *args):
    # check if the message is from a real player
    # if username == bot.username:
    # return
    # print the message
    print(username + ':', message)
    messages_listbox.insert(tk.END, f"{username}: {message}")

    if message == ';startafk':
        start_afk()
    elif message == ';stopafk':
        stop_afk()


# listen for incoming chat messages
bot.on('chat', handle_chat)


def send_chat_message():
    message = message_entry.get()
    bot.chat(message)
    message_entry.delete(0, tk.END)


def start_afk():
    print("Starting AFK...")
    bot.chat("Starting AFK...")
    bot.setControlState('forward', True)
    bot.setControlState('jump', True)


def stop_afk():
    print("Stopping AFK...")
    bot.chat("Stopping AFK...")
    bot.clearControlStates()


window = tk.Tk()
window.title("Minecraft Chatbot")
window.geometry("850x500+100+100")

server_chat_label = tk.Label(window, text="Server Chat: ", font=('Arial', 14, 'normal'), anchor='w')
server_chat_label.pack(side='left', padx=10, pady=10)

# create a frame to hold the listbox and scrollbar
listbox_frame = tk.Frame(window)
listbox_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

# create the listbox and scrollbar
messages_listbox = tk.Listbox(listbox_frame, font=('Arial', 12), height=0)
messages_listbox.pack(side='left', fill='both', expand=True)
scrollbar = tk.Scrollbar(listbox_frame, command=messages_listbox.yview)
scrollbar.pack(side='right', fill='y')
messages_listbox.config(yscrollcommand=scrollbar.set)

# create the label and entry for sending messages
message_label = tk.Label(window, text="Enter message:", font=('Arial', 12))
message_label.pack(pady=10)
message_entry = tk.Entry(window, font=('Arial', 12))
message_entry.pack(fill=tk.X, padx=20)

# create the button for sending messages
send_button = tk.Button(window, text="Send", command=send_chat_message, font=('Arial', 12))
send_button.pack(pady=10)

# start the GUI main loop
window.mainloop()
