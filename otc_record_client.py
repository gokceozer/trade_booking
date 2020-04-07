import tkinter as tk
from tkinter import ttk
import socket
import threading
import sys
import struct

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverName = '192.168.101.210'
serverPort = 6024


class Page(tk.Frame):
    def __init__(self,root):
        tk.Frame.__init__(self,width=900, height=800)
        self.root=root
    def show(self):
        self.lift()


class Page1(Page):
   def __init__(self, root, Page2):
       Page.__init__(self,root)
       self.Page2 = Page2

       #Create Labels
       lbl_time = tk.Label(self, text="Time").grid(row=0, column=0)
       lbl_exchange = tk.Label(self, text="Exchange").grid(row=0, column=1)
       lbl_amount = tk.Label(self, text="Amount").grid(row=0, column=2)
       lbl_price = tk.Label(self, text="Price").grid(row=0, column=3)
       lbl_buy_sell = tk.Label(self, text="Buy/Sell").grid(row=0, column=4)
       lbl_symbol = tk.Label(self, text="Symbol").grid(row=0, column=5)
       lbl_commission = tk.Label(self, text="Commission").grid(row=0, column=6)
       lbl_commission_currency = tk.Label(self, text="Commission Currency").grid(row=0,
                                                                               column=7)
       lbl_commission_to_BTC = tk.Label(self, text="Commission-BTC Rate").grid(row=0,
                                                                               column=8)

       change_of_USDT = tk.Label(self, text="Change of USDT").grid(row=3, column=0)


       cum_change_of_USDT = tk.Label(self, text="Cumulative change of USDT").grid(row=3,
                                                                                column=1)



       lbl_notes = tk.Label(self, text="Notes").grid(row=3, column=2)

       self.text = tk.StringVar()
       self.error = tk.Label(self, textvariable = self.text).grid(row=6, column=0)


       self.time_input = tk.Entry(self, width=15)
       self.time_input.grid(row=1, column=0)
       self.exchange_input = tk.Entry(self, width=15)
       self.exchange_input.grid(row=1, column=1)
       self.amount_input = tk.Entry(self, width=15)
       self.amount_input.grid(row=1, column=2)
       self.price_input = tk.Entry(self, width=15)
       self.price_input.grid(row=1, column=3)

       self.side = ["BUY", "SELL"]
       self.variable = tk.StringVar(self)
       self.variable.set(self.side[0]) # default value
       w = ttk.OptionMenu(self, self.variable, "BUY",*self.side)
       w.grid(row=1, column=4)

       self.symbol_input = tk.Entry(self, width=15)
       self.symbol_input.grid(row=1, column=5)
       self.commission_input = tk.Entry(self, width=15)
       self.commission_input.grid(row=1, column=6)
       self.commission_currency_input = tk.Entry(self, width=15)
       self.commission_currency_input.grid(row=1, column=7)
       self.commission_to_BTC_input = tk.Entry(self, width=15)
       self.commission_to_BTC_input.grid(row=1, column=8)


       self.text_USDT = tk.StringVar()
       change_of_USDT_res = tk.Label(self, textvariable = self.text_USDT).grid(row=4, column=0)
       self.text_USDT_cum = tk.StringVar()
       cum_change_of_USDT_res = tk.Label(self, textvariable = self.text_USDT_cum).grid(row=4,column=1)

       self.notes_input = tk.Entry(self, width=15)
       self.notes_input.grid(row=4, column=2)

       clear_button = ttk.Button(self, text="Clear",command=self.clear).grid(row=4, column=6)
       button_calc = ttk.Button(self, text="Calculate",command=self.calculateUSDT).grid(row=4, column=7)
       button = ttk.Button(self, text="Submit",command=self.submit_trade).grid(row=4, column=8)



   def clear(self):
       self.time_input.delete(0, 'end')
       self.exchange_input.delete(0, 'end')
       self.amount_input.delete(0, 'end')
       self.price_input.delete(0, 'end')
       self.variable.set(self.side[0]) # default value
       self.symbol_input.delete(0, 'end')
       self.commission_input.delete(0, 'end')
       self.commission_currency_input.delete(0, 'end')
       self.commission_to_BTC_input.delete(0, 'end')
       self.text_USDT.set("")
       self.text_USDT_cum.set("")
       self.notes_input.delete(0, 'end')

   def submit_trade(self):

       trade_message = str(self.time_input.get()) + "," + self.exchange_input.get() + "," + str(self.amount_input.get()) \
       + "," + str(self.price_input.get()) + "," + self.variable.get() + "," + self.symbol_input.get() + "," \
       + str(self.commission_input.get()) + "," + self.commission_currency_input.get() + "," + str(self.commission_to_BTC_input.get()
       + "," +  str(self.text_USDT.get()) + "," + str(self.text_USDT_cum.get()) + "," + str(self.notes_input.get()))
       clientSocket.send(trade_message.encode())

       print("Client sending trade order:")
       print(repr(trade_message))

       self.clear()



   def calculateUSDT(self):
       if "USD" in self.symbol_input.get():
           if len(self.amount_input.get())>0 and len(self.price_input.get())>0:
               if self.variable.get() == "BUY":
                   self.text_USDT.set(round(-1 * self.convert(self.amount_input.get()) * self.convert(self.price_input.get()),5))
               else:
                   self.text_USDT.set(round(self.convert(self.amount_input.get()) * self.convert(self.price_input.get()),5))

               if self.Page2.cum_USDT == 0:
                   self.text_USDT_cum.set(self.text_USDT.get())
               else:
                    self.text_USDT_cum.set(str(float(self.text_USDT.get()) + self.Page2.cum_USDT))

           else:
               self.text.set('Please input Amount, Price and Direction to calculate')
       else:
           #self.error.config(text="Please input Amount, Price and Direction to calculate")
           self.text_USDT.set("0")
           self.text_USDT_cum.set(self.Page2.cum_USDT)

   def convert(self, s):
    try:
        return float(s)
    except:
        num, denom = s.split('/')
        return float(num) / float(denom)



class Page2(Page):
    def __init__(self, root):
        Page.__init__(self,root)

        self.grid(sticky='news')

        self.frame_canvas = tk.Frame(self, width=1500, height=1500)
        self.frame_canvas.grid(sticky='news')
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        self.frame_canvas.grid_propagate(True)

        # Add a canvas in that frame
        self.canvas = tk.Canvas(self.frame_canvas, width=1300, height=700,scrollregion=(0,0,200,200))
        self.canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        self.vsb = tk.Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)







        self.all_trades_text = tk.StringVar()
        self.root = root
        self.receive_thread = threading.Thread(target=self.receive, args=(clientSocket,))
        self.receive_thread.setDaemon(True)
        self.receive_thread.start()
        self.cum_USDT = 0.0




    def receive(self, client_socket):
        """Handles receiving of messages."""



        #try:
        while True:
            
            tmp = client_socket.recv(8)  # Header size
            (length,) = struct.unpack('>Q', tmp)  # Parse payload length
            payload = b''
            while len(payload) < length:
                print("Here")
                to_read = length - len(payload)
                payload += client_socket.recv(4096 if to_read > 4096 else to_read)
                print("Here1")

            msg = payload.decode()
            print("MSG:")
            print(msg)

            self._widgets = []

            # Create a frame to contain the buttons
            frame_buttons = tk.Frame(self.canvas, bg="blue", width=1300, height=1300)
            self.canvas.create_window((0, 0), window=frame_buttons, anchor='n')
            # Add 9-by-5 buttons to the frame
            column = 0
            row = 0
            rows = msg.count('\n')
            columns = 12
            print(rows)
            buttons = [[tk.Label() for j in range(columns)] for i in range(rows+1)]



            for trade in msg.splitlines():
                #print("row = %d, column = %d" % (row, column))
                print(trade)
                current_trade = trade.split(",")
                for i in range(1, len(current_trade)-1):
                    j = current_trade[i].replace(' ','')
                    current_trade[i] = j
                print("Client receiving trade order:")
                print(repr(current_trade))
                column = 0
                current_row = []

                for column in range(0, columns):
                    print("row %s column %s" % (row,column))
                    if column in (7,8,9,10,11):
                        buttons[row][column] = tk.Label(frame_buttons, text=current_trade[column], borderwidth=0, width=14)
                        buttons[row][column].grid(row=row, column=column, sticky='news', padx=1, pady=1)
                    elif column !=4:
                        buttons[row][column] = tk.Label(frame_buttons, text=current_trade[column], borderwidth=0, width=10)
                        buttons[row][column].grid(row=row, column=column, sticky='news', padx=1, pady=1)
                    else:
                        buttons[row][column] = tk.Label(frame_buttons, text=current_trade[column], borderwidth=0, width=6)
                        buttons[row][column].grid(row=row, column=column, sticky='news', padx=1, pady=1)


                    if row == 1 and  column == columns-2:
                        self.cum_USDT = round(float(current_trade[column]),5)


                row += 1

            frame_buttons.update_idletasks()

            # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
            first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, 5)])
            first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, 5)])
            self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                                height=first5rows_height)

            # Set the canvas scrolling region
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
                    #self._widgets.append(current_row)

                #for i in range(11):
                    #self.top_frame.grid_columnconfigure(i, weight=1)

        #except:
            #e = sys.exc_info()
            #print(e)
        on_closing()





class MainView(tk.Frame):
    def __init__(self,root):
        tk.Frame.__init__(self, root, width=900, height=800)
        #self.place(height=800, width=1300)
        p2 = Page2(root)
        p1 = Page1(root, p2)


        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = ttk.Button(buttonframe, text="Enter New Trade", command=p1.lift)
        b2 = ttk.Button(buttonframe, text="OTC Trade List", command=p2.lift)

        b1.pack(side="left")
        b2.pack(side="left")

        p1.show()


def on_closing():
    clientSocket.close()
    root.destroy()



if __name__ == "__main__":

    clientSocket.connect((serverName, serverPort))

    root = tk.Tk()
    root.grid_rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)


    root.protocol('WM_DELETE_WINDOW', on_closing)
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1400x800")





    root.mainloop()