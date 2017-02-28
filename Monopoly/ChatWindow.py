import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from threading import Thread


class ChatWindow(Thread):

    def __init__(self, width, height, send_chat=None):
        Thread.__init__(self, daemon=True)

        # Set up variables inside init
        self.width = width
        self.height = height

        # Save the external chat function
        if not send_chat:
            send_chat = self.add_to_log
        self.send_chat = send_chat

        # Window components
        self.root = None
        self.log = None
        self.chat_var = None

        self.start()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', lambda: 0)

        self.root.title("Monopoly Chat Window")
        self.root.resizable(0, 0)

        # Add a frame
        log_frame = tk.LabelFrame(self.root, text="Chat Log", width=self.width, height=(3 * self.height) / 4)
        log_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add the scrolledtext widget
        log = scrolledtext.ScrolledText(log_frame, state=tk.DISABLED)
        log.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.log = log

        # Add a normal text widget to the bottom to send messages
        chat_frame = tk.Frame(self.root, width=self.width, height=(self.height / 4))
        chat_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add the text widget
        self.chat_var = tk.StringVar()
        chat_box = tk.Entry(chat_frame, textvariable=self.chat_var)
        chat_box.bind('<Return>', self.chat)
        chat_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        send_button = tk.Button(chat_frame, text="Send", command=self.chat)
        send_button.pack(side=tk.LEFT, fill=tk.BOTH)

        self.root.mainloop()

    def add_to_log(self, msg, player=None):
        # The default '>>' will precede server events
        if player is None:
            prefix = '>>'
        else:
            prefix = '[%s]:' % player
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, prefix + " " + msg + '\n')
        self.log.config(state=tk.DISABLED)

    def chat(self, *args):
        """
        Gets a message from the chat box and sends the message to the server
        :param args: Any extra args (used to escape event args from the Return key binding
        :return: None
        """
        # Get the text from the entry
        message = self.chat_var.get()
        if message:
            self.send_chat(message)
        self.chat_var.set("")

    def destroy(self):
        self.root.quit()


if __name__ == '__main__':
    chat = ChatWindow(500, 720)
