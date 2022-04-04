from tkinter import *
import json
import customtkinter  # <- import the CustomTkinter module
from tkinter import filedialog as fd
from tkinter import ttk

TEST_CONFIGURE = True
TEST_REMOVING = False

root_tk = customtkinter.CTk()
root_tk.geometry("")
root_tk.resizable(width=False, height=False)
root_tk.title("ProxViewer for MiFare 1K")
style = ttk.Style()


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
    labelData = customtkinter.CTkLabel(root_tk, width=200, text="no data...", justify=LEFT)
    labelData.config(font=("Courier", 12))
    labelData["text"] = "UID:\t" + data["Card"]["UID"] + "\nType:\t" + data["FileType"] + "\nSAK:\t" + data["Card"][
        "SAK"] + "\nATQA:\t" + data["Card"]["ATQA"]
    labelData.pack(pady=10)


def setup():
    initialButton = customtkinter.CTkButton(root_tk, width=500, height=50, text="Select JSON Dump File",
                                            command=selectFile)
    initialButton.pack(pady=20)

    if TEST_CONFIGURE: initialButton.configure(text="Select JSON Dump File")
    if TEST_REMOVING: initialButton.configure(text="no file selected")

    label = customtkinter.CTkLabel(root_tk, width=200, text="no file selected", text_color="#808080")
    label.config(font=("Courier", 12))
    label.pack(pady=10)


def selectFile():
    for widget in root_tk.winfo_children():
        widget.destroy()

    fileDir = customtkinter.CTkButton(root_tk, width=500, height=50, text="Select JSON Dump File", command=selectFile)
    fileDir.pack(pady=20)
    if TEST_CONFIGURE: fileDir.configure(text="Select JSON Dump File")
    if TEST_REMOVING: fileDir.configure(text="no file selected")

    label = customtkinter.CTkLabel(root_tk, width=200, text="no file selected", text_color="#808080")
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
