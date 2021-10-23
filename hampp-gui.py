import os
import decimal
import tkinter as tk
import tkinter.ttk as ttk

from threading import Thread as th
from secrets import randbelow

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

class HamppGuiApp:

    workLock = False

    def __init__(self, master=None):
        # 1. Set up gui

        # build ui
        self.frame1 = ttk.Frame(master)

        # This is the entry for your investment size
        self.money_entry = ttk.Entry(self.frame1)
        self.money_entry.place(anchor='nw', relwidth='0.22', relx='0.25', rely='0.07', x='0', y='0')
        
        # This is the label for the above entry
        self.money_label = ttk.Label(self.frame1)
        self.money_label.configure(text='Total to Invest:     $')
        self.money_label.place(anchor='nw', relwidth='0.22', relx='0.03', rely='0.073', x='0', y='0')
        
        # This is the textbox that contains the Hamster's wisdom
        self.guidance = tk.Text(self.frame1)
        self.guidance.configure(height='10', width='70', wrap='word')
        self.guidance.place(anchor='nw', relx='0.01', rely='0.51', x='0', y='0')
        self.guidance.config(state='disabled')
        
        # This is the label for the below entry
        self.howMany_label = ttk.Label(self.frame1)
        self.howMany_label.configure(text='Total to Select:     #')
        self.howMany_label.place(anchor='nw', relwidth='.23', relx='0.03', rely='0.2', x='0', y='0')
        
        # This is the entry for the number of crypto to select
        self.how_many = ttk.Entry(self.frame1)
        self.how_many.place(anchor='nw', relwidth='0.22', relx='0.25', rely='0.194', x='0', y='0')
        
        # Button that makes Hamster dispel wisdom
        self.wisdom_button = ttk.Button(self.frame1)
        self.wisdom_button.configure(text='Recieve the Hamster\'s Wisdom')
        self.wisdom_button.place(anchor='nw', relwidth='0.94', relx='0.01', rely='0.42', width='0', x='0', y='0')
        self.wisdom_button.configure(command=lambda: self.workThread(op='teach'))
        
        # The glorious Sir Hamster, the Great
        self.label5 = ttk.Label(self.frame1)
        self.hampic180_png = tk.PhotoImage(file='hampic-180.png')
        self.label5.configure(image=self.hampic180_png, text='label5')
        self.label5.place(anchor='nw', relheight='0.41', relx='0.66', x='0', y='0')

        # Main frame
        self.frame1.configure(height='400', width='600')
        self.frame1.pack(side='top')

        # Main widget
        self.mainwindow = self.frame1
    
        # 2. Set up system
        self.cryptos = self.getList()
        if self.cryptos == 'FUK':
            print('List document malformed. Be sure to separate items by newline.')
            exit()  # Crash app if list is malformed

    def workThread(self, op):
        """
        This function directs commands to their threads, or rejects them if currently working.

        :param op: Specifies the type of operation
        :return: None
        """
        if op == 'teach':
            self.workLock = True
            work = th(self.buy())
            try:
                work.start()

            except Exception as e:
                self.setText(self.guidance, str(e))
                self.workLock = False

    def getList(self):
        """
        This function generates a list of cryptos based on whatever file is called "list"
        :return: List of strings (crypto names)
        """
        try:
            if os.path.isfile('list'):
                with open('list') as file:
                    cryptos = file.read().split('\n')
                    cryptos.remove('')  # Remove empty elements if they appear
                    size = len(cryptos)
                    return cryptos  # Return the list and the number of elements within it

            else:
                return 'FUK'

        except:
            return 'FUK'

    def getInfo(self):
        try:
            money = self.money_entry.get()
            money = float(money)
        except:
            self.setText(self.guidance, 'Put a decimal ($x.xx) into money entry')
            return 'FUK'

        try:
            howMany = self.how_many.get()
            howMany = int(howMany)
        except:
            self.setText(self.guidance, 'Put an integer (whole number) into "Total to Select" entry')
            return 'FUK'

        return (money, howMany)

    def buy(self):
        stuff = self.getInfo()
        if stuff == 'FUK':
            self.workLock = False
            return

        howMany = stuff[1]
        money = stuff[0]

        cryptoList = self.cryptos
        size = len(cryptoList)
        response = ''

        if howMany > size:
            response += 'You asked to select more cryptos than I know about. I\'ll choose 5 instead.\n'
            howMany = 5

        elif howMany < 1:
            response += 'If you didn\'t want to invest, why bother asking?\n'
            self.setText(self.guidance, response)
            self.workLock = False  # Release worklock
            return

        dVal = decimal.Decimal  # Create a decimal object
        cent = dVal('0.01')  # Create placeholder
        invest = money / howMany  # Do mafs
        invest = float(dVal(str(invest)).quantize(cent, rounding=decimal.ROUND_UP))  # Round to nearest cent

        portfolio = []  # Empty list will hold selected cryptos

        for x in range(howMany):  # Depending on how many you want, select that many.
            while True:  # Keep on trying until a unique crypto is selected (avoid doubletap)
                selection = cryptoList[randbelow(size)]
                if not selection in portfolio:
                    portfolio.append(selection)
                    break

                else:
                    pass

        response += 'Buy $' + str(invest) + ' of:\n'
        for item in portfolio:
            response += '\t[+]   ' + str(item) + '\n'

        self.setText(self.guidance, response)
        self.workLock = False

    def setText(self, where, text):
        """
        This sets text of textbox.

        :param text: What you want to display
        :param where: tkEntry object ; 'password' = password textbox.
        :return: None
        """
        where.config(state='normal')
        where.delete('1.0', 'end')
        where.insert('0.0', text)
        where.config(state='disabled')  # Re-lock display



    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(height=False, width=False)  # Prohibit resizing
    root.wm_title('Hamster++ v0.1')


    app = HamppGuiApp(root)
    app.run()


