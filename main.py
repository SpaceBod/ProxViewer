from tkinter import *
import json
from tkinter import filedialog as fd
from tkinter import ttk
import os

root_tk = Tk()
root_tk.geometry("")
root_tk.resizable(width=False, height=False)
root_tk.configure(background="#1f1f1f")
root_tk.title("ProxViewer for MiFare 1K")
style = ttk.Style()



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

buttonImage = resource_path("buttonImg.png")
buttonImg = PhotoImage(file = buttonImage)

def insertSpaces(string, integer, spaceType):
    if spaceType == 0:
        return string[0:integer] + '   ' + string[integer:]
    else:
        return string[0:integer] + ' ' + string[integer:]


def createTable(data, pos, rowStart, rowEnd, sectorStart):
    style.theme_use("clam")
    table = ttk.Treeview(root_tk, height=40)
    style.configure("Treeview", font=("Consolas", 12), background="#1f1f1f", fieldbackground="black",
                    foreground="white")
    style.configure("Treeview.Heading", font=("Consolas", 12), background="#1f1f1f", foreground="white")
    table['columns'] = ('Block', 'Data')

    table.column("#0", width=0, stretch=NO)
    table.column("Block", anchor=CENTER, width=80)
    table.column("#0", width=0, stretch=NO)
    table.column("Data", anchor=CENTER, width=360)

    table.heading("#0", text="", anchor=CENTER)
    table.heading("Block", text="Block", anchor=CENTER)
    table.heading("#0", text="", anchor=CENTER)
    table.heading("Data", text="Data", anchor=CENTER)

    table.insert(parent='', index='end', iid=0, text='', values=('', 'S' + str(sectorStart)), tags=('SectorName',))

    sectorNew = 0
    blockCount = rowStart
    offset = 1
    for x in range(rowStart, rowEnd):
        dataValue = data["blocks"][str(blockCount)]

        if sectorNew == 3:
            dataValue = insertSpaces(insertSpaces(insertSpaces(dataValue, 12, 0), 23, 0), 19, 1)
            table.insert(parent='', index='end', iid=x + offset - rowStart, text='',
                         values=(blockCount, dataValue), tags=('Trailer',))
            table.insert(parent='', index='end', iid=x + offset + 1 - rowStart, text='',
                         values=('', 'S' + str(int(offset) + int(sectorStart))), tags=('SectorName',))
            sectorNew = 0
            offset += 1
        else:
            dataValue = ' '.join([dataValue[i:i + 4] for i in range(0, len(dataValue), 4)])
            table.insert(parent='', index='end', iid=x + offset - rowStart, text='',
                         values=(blockCount, dataValue))
            sectorNew += 1
        blockCount += 1

    table.delete(len(table.get_children()) - 1)
    table.tag_configure('Trailer', foreground='green')
    table.tag_configure('SectorName', foreground='#1c94cf', background='#363636')
    table.pack(side=pos)


def displayData(data):
    labelData = Label(root_tk, width=50, text="no data...", justify=LEFT, bg="#1f1f1f", fg='yellow')
    labelData.config(font=("Courier", 12))
    labelData["text"] = "UID:\t" + data["Card"]["UID"] + "\nType:\t" + data["FileType"] + "\nSAK:\t" + data["Card"][
        "SAK"] + "\nATQA:\t" + data["Card"]["ATQA"]
    labelData.pack(pady=10)


def setup():
    initialButton = Button(root_tk, text="Select JSON Dump File", command=selectFile, image = buttonImg, highlightthickness = 0, bd = 0)
    initialButton.pack(pady=20)

    label = Label(root_tk, width=20, text="no file selected", fg="#808080", bg="#1f1f1f")
    label.config(font=("Courier", 12))
    label.pack(pady=10)


def selectFile():
    for widget in root_tk.winfo_children():
        widget.destroy()

    fileDir = Button(root_tk, text="Select JSON Dump File", command=selectFile, image = buttonImg, highlightthickness = 0, bd = 0)
    fileDir.pack(pady=20)

    label = Label(root_tk, text="no file selected", fg="#808080", bg="#1f1f1f")
    label.config(font=("Courier", 12))
    label.pack(pady=10)

    filetypes = (
        ('text files', '*.json'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a JSON file',
        initialdir='/',
        filetypes=filetypes)

    label['text'] = filename.split("/")[-1]
    with open(filename) as f:
        data = json.load(f)

    displayData(data)
    createTable(data, LEFT, 0, 32, 0)
    createTable(data, RIGHT, 32, 64, 8)


def main():
    setup()
    root_tk.mainloop()


main()
