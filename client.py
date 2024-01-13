import socket
from tkinter import *
import tkinter as tk
from threading import Thread
from PIL import ImageTk, Image
import random
import platform

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None

canvas1 = None
canvas2=None

playerName = None
nameEntry = None
nameWindow = None

gameWindow=None
ticketGrid  = []
currentNumberList = []
flashNumberList = []
flashNumberLabel = None

def createTicket():
    global gameWindow
    global ticketGrid
    # Ticket Frame
    mianLable = Label(gameWindow, width=65, height=16,relief='ridge', borderwidth=5, bg='white')
    mianLable.place(x=95, y=119)

    xPos = 105
    yPos = 130
    for row in range(0, 3):
        rowList = []
        for col in range(0, 9):
            if(platform.system() == 'Darwin'):
                # For Mac users
                boxButton = Button(gameWindow,
                font = ("Chalkboard SE",18),
                borderwidth=3,
                pady=23,
                padx=-22,
                bg="#fff176",
                highlightbackground='#fff176',
                activebackground='#c5e1a5')


                boxButton.place(x=xPos, y=yPos)
            else:
                # For windows users
                boxButton = tk.Button(gameWindow, font=("Chalkboard SE",30), width=3, height=2,borderwidth=5, bg="#fff176")
                boxButton.place(x=xPos, y=yPos)

            rowList.append(boxButton)
            xPos += 64
        ticketGrid.append(rowList)
        xPos = 105
        yPos +=82

def placeNumbers():
    global ticketGrid
    global currentNumberList

    for row in range(0,3):
        randomColList = []
        counter = 0
        while counter<=4:
            randomCol = random.randint(0,8)
            if(randomCol not in randomColList):
                randomColList.append(randomCol)
                counter+=1

        numberContainer = {
        "0": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "1": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "2": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
        "3": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
        "4": [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        "5": [50 , 51, 52, 53, 54, 55, 56, 57, 58, 59],
        "6": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
        "7": [70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
        "8": [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
        }    

        counter = 0
        while (counter < len(randomColList)):
            colNum = randomColList[counter]
            numbersListByIndex = numberContainer[str(colNum)]
            randomNumber = random.choice(numbersListByIndex)

            if(randomNumber not in currentNumberList):
                numberBox = ticketGrid[row][colNum]
                numberBox.configure(text=randomNumber, fg="black")
                currentNumberList.append(randomNumber)

                counter+=1


def gameWindow():
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global flashNumberLabel

    gameWindow = Tk()
    gameWindow.title("Tambola Family Fun")
    gameWindow.geometry('800x600')

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "assets/background.jpg")

    canvas2 = Canvas( gameWindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)

    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    canvas2.create_text( screen_width/4.5,50, text = "Tambola Family Fun", font=("Chalkboard SE",50), fill="#3e2723")

    createTicket()
    placeNumbers()

    flashNumberLabel = canvas2.create_text(400,screen_height/2.3, text = "Waiting for other players to join...", font=("Chalkboard SE",30), fill="#3e2723")

    gameWindow.resizable(True, True)
    gameWindow.mainloop()

def save_name():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName=nameEntry.get()
    nameEntry.delete(0,END)
    nameWindow.destroy()
    SERVER.send(playerName.encode())

def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1
    global screen_width
    global screen_height

    nameWindow=Tk()
    nameWindow.title("Tambola family fun")
    nameWindow.geometry("800x600")

    screen_width=nameWindow.winfo_screenwidth()
    screen_height=nameWindow.winfo_screenheight()

    bg=ImageTk.PhotoImage(file="./assets/background.jpg")
    canvas1=Canvas(nameWindow,width=500,height=500)
    canvas1.pack(fill="both",expand=True)
    canvas1.create_image(0,0,image=bg,anchor="nw")
    canvas1.create_text(screen_width/4,screen_height/6,text="Enter Name",font=("Chalkboard SE",50),fill="blue")

    nameEntry=Entry(nameWindow,width=15,justify="center",font=("Chalkboard SE",30),bg="white")
    nameEntry.place(x=200,y=300)

    button=Button(nameWindow,text="SAVE",font=("Chalkboard SE",30),width=10,command=save_name,height=2,bg="#80deea",bd=3)
    button.place(x=screen_width/6,y=400)


    nameWindow.resizable(True,True)
    nameWindow.mainloop()

def recivedMsg():
    pass

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 6000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    thread = Thread(target=recivedMsg)
    thread.start()

    askPlayerName()

setup()