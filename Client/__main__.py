from sys import exit, stderr
from tkinter import *
try:
    from .main import Main
except SystemError:
    stderr.write("Monopoly.Client [ERROR]: Client must be run as a module. "
                 "See https://crnbrdrck.github.io/Monopoly/ for instructions")
    exit(1)

"""
Allows for running the code using python3 -m Client
"""
def main():
    gui = Main()
    window = Tk()
    window.title("Monopoly")
    host = StringVar()
    host.set("127.0.0.1")
    name = StringVar()
    name.set("Guest")
    password = StringVar()


    def create():
        password_text = password.get()
        password_text = password_text if password_text != '' else None
        gui.create(host.get(), name.get(), password_text)
        run()


    def join():
        password_text = password.get()
        password_text = password_text if password_text != '' else None
        gui.join(host.get(), name.get(), password_text)
        run()


    def poll():
        print("Polling the network for games")
        servers = gui.poll()
        if not servers:
            print("No Servers running")
        else:
            for server in servers:
                print(server)


    def run():
        # Now run the game
        window.destroy()
        gui.init_display()
        gui.run()

    f = LabelFrame(window, text="Host IP")
    Entry(f, textvariable=host).pack(side=TOP, fill=BOTH, expand=1)
    f.pack(side=TOP, fill=BOTH, expand=1)
    f = LabelFrame(window, text="Username")
    Entry(f, textvariable=name).pack(side=TOP, fill=BOTH, expand=1)
    f.pack(side=TOP, fill=BOTH, expand=1)
    f = LabelFrame(window, text="Password")
    Entry(f, textvariable=password).pack(side=TOP, fill=BOTH, expand=1)
    f.pack(side=TOP, fill=BOTH, expand=1)
    Button(window, text="Create", command=create).pack(side=TOP, fill=BOTH, expand=1)
    Button(window, text="Join", command=join).pack(side=TOP, fill=BOTH, expand=1)
    Button(window, text="Poll for Games", command=poll).pack(side=TOP, fill=BOTH, expand=1)
    window.mainloop()

if __name__ == '__main__':
    main()
