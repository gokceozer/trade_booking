import socket
import threading
import csv
import os
import logging
import time
import pandas as pd
threads = []

mutex = threading.Lock()

fieldnames = ['Time', 'Exchange', 'Amount', 'Price', 'Side', 'Symbol', 'Commission',
'Commission_Currency', 'Commission_to_BTC', 'Change_of_USDT', 'Change_Cumulative_USDT', 'Notes']

cum_change_of_USDT = 0



class ServerThread(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
        self.handled = False

    def print_csv(self):
        print("PRINTING CSV")
        with open('otc_trade_records.csv', "r+", newline='') as f:
            data=f.read()
            print(data)

    def clean_up(self):
        with open('otc_trade_records.csv') as f1:

            with open('otc_trade_records_copy.csv', "w+") as f2:
                for line in f1.readlines():
                    if len(set(line.strip())) == 1:
                        continue
                    f2.write(line)
        os.rename('otc_trade_records_copy.csv', 'otc_trade_records.csv')


    def send_past_trades(self):
        #self.clean_up()
        #try:
        #self.print_csv()
        with open('otc_trade_records.csv',newline='') as f:
            connectionSocket, addr = self.client
            while(True):
                trades = f.read(1024)
                if trades == "":
                    break
                print("sending:")
                print(trades)
                connectionSocket.send(trades.encode())
            
            
        #self.print_csv()


    def append_to_csv(self, trade):
        with open('otc_trade_records.csv', 'a') as fd:
            fd.write("\n")
            fd.write(trade)

    def run(self):
        connectionSocket, addr = self.client

        mutex.acquire()
        self.send_past_trades()
        mutex.release()



        #try:
        #connectionSocket.send(past_trades.encode())
        #except:
            #print("Could not send the message")


        trade = "initial"

        while(trade != ""):
            #try:
            print("Client sent:")
            trade = connectionSocket.recv(1024).decode()
            print(trade)
            if trade != "":
                self.append_to_csv(trade)
            #self.print_csv()

            for thread in threads:
                thread.send_past_trades()


            #except:
               # print("Error while receiving message")


        connectionSocket.close()

        self.handled = True

class ServerMain:
    def server_run(self):


        serverPort = 6024
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind( ("", serverPort) )
        serverSocket.listen(5)
        logging.info("The server is ready to receive")
        global threads
        while True:
            for t in threads:
                if  t.handled == True:

                    threads = [t for t in threads if not t.handled]
                    t.join()

            try:
                client = serverSocket.accept()
            except ConnectionResetError as err:
                logging.info("Connection Reset")
                os._exit(0)
            except:
                logging.debug("An error occured in Server")
                os._exit(0)

            t = ServerThread(client)
            threads.append(t)
            t.start()


        serverSocket.close()
        self.handled = True



if __name__ == '__main__':
    logging.basicConfig(filename='server_error.log', format='%(asctime)s %(levelname)-8s %(message)s'
                        ,datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)



    server = ServerMain()
    server.server_run()
