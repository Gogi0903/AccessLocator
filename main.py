import pandas
from tkinter import *
from tkinter import messagebox

# template: https://docs.google.com/spreadsheets/d/1pW2gfjfCxpZOy0ILitlRd86ji6qjkwUr0kKfno_ofuk/edit#gid=0

FONT = ('Arial', 24, 'bold')
SHEET_ID = "1pW2gfjfCxpZOy0ILitlRd86ji6qjkwUr0kKfno_ofuk"
SHEET_NAME = "Munkalap1"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"


def get_datas():
    # kiolvassa az adatokat az excelből
    datas = pandas.read_csv(URL)
    return datas


def is_user(name):
    # megvizsgálja, hogy az adott user-nek van e hozzáférése
    data = get_datas()
    users = data["user"].to_list()
    user_list = [user for user in users if isinstance(user, str)]
    if name in user_list:
        return True
    else:
        messagebox.showinfo(title="Hiba!", message=f"A(z) '{name}' nevű felhasználó nem létezik.")


def user_sec_lvl(name):
    # visszaadja az adott user sec lvl-ét integerként
    data = get_datas()
    users = data["user"].to_list()
    user_lvl = data["user_sec_lvl"].to_list()
    users_dict = {key: int(value) for key, value in zip(users, user_lvl) if isinstance(key, str)}
    your_lvl = users_dict[name]
    return your_lvl


def links_kw(keywords):
    # listába válogatja a megadott kulcsszavaknak megfelelő linkeket
    links = []
    data = get_datas()
    video_keywords = data["keyword"].to_list()
    video_links = data['link'].to_list()
    for kw in keywords:
        for vid_kw, vid_link in zip(video_keywords, video_links):
            if kw in vid_kw.split(", "):
                links.append(vid_link)
    return list(set(links))


def links_sec_lvl():
    # listába válogatja a user sec lvl-nek megfelelő linkeket
    data = get_datas()
    your_lvl = user_sec_lvl(name=user_id_entry.get())
    video_sec_lvl = data['security_level'].to_list()
    video_links = data['link'].to_list()
    links = [vid_link for vid_sec_lvl, vid_link in zip(video_sec_lvl, video_links) if your_lvl >= vid_sec_lvl]
    return links


def link_to_print(keys):
    # listába válogatja a sec lvl-nek és kw-nek megfelelő linkeket
    vid_kw = links_kw(keywords=keys)
    vid_lvl = links_sec_lvl()
    links = [link for link in vid_kw if link in vid_lvl]
    return links


def entry_checker(entry):
    # megvizsgálja, hogy ki van e töltve a mező
    if len(entry) == 0:
        messagebox.showinfo(title="Hiba!", message="Kérlek add meg a kért adatokat")
    else:
        return True


def return_entry(entry):
    # visszaadja a mezőbe írtakat listába szedve
    words = entry.replace(" ", "").split(",")
    if "" in words:
        words.remove("")
    words = [word.lower() for word in words]
    return words


def continue_bt():
    # a tovább gomb commandja
    user = user_id_entry.get()
    if entry_checker(entry=user) and is_user(name=user):
        window_2 = Toplevel(window)
        window_2.title("Kulcsszavak")
        window_2.config(padx=50, pady=50)
        window_2.grab_set()

        welcome_label = Label(window_2, text=f"Szia {user}!", font=('Arial', 12, 'bold'))
        welcome_label.grid(row=0, column=0, columnspan=2)

        welcome_label_2 = Label(window_2,
                                text="Kérlek add meg a keresendő szavakat vesszővel elválasztva!",
                                font=('Arial', 12))
        welcome_label_2.grid(row=1, column=0, columnspan=2, pady=20)

        welcome_label_3 = Label(window_2, text="Kulcsszavak: ", font=('Arial', 16))
        welcome_label_3.grid(row=2, column=0)

        kw_entry = Entry(window_2, width=40)
        kw_entry.grid(row=2, column=1)

        search_b = Button(window_2, text="Keresés",
                          command=lambda: search_button(link=return_entry(entry=kw_entry.get())))
        search_b.grid(row=3, column=1)

        window_2.mainloop()


def search_button(link):
    # kidobja a keresési eredményeket
    if entry_checker(entry=link):
        links_list = link_to_print(keys=link)

        window_3 = Tk()
        link_for_window_3 = Text(window_3)
        link_nr = 0
        for elem in links_list:
            link_nr += 1
            elem_to_insert = f"Link {link_nr}:\n{elem}\n\n"
            link_for_window_3.insert(END, elem_to_insert)
        link_for_window_3.config(state=DISABLED)
        link_for_window_3.pack(padx=20, pady=20)

        window_3.mainloop()


window = Tk()
window.title("Videó-keresőprogram")
window.config(padx=50, pady=50)

welcome_text_1 = Label(text="Üdvözöllek!", font=FONT)
welcome_text_1.grid(row=0, column=0, pady=20, columnspan=2)

welcome_text_2 = Label(text="Kérlek add meg a User ID-dat!", font=('Arial', 12))
welcome_text_2.grid(row=1, column=0, columnspan=2)

user_id = Label(text="User ID:", font=('Arial', 16))
user_id.grid(row=2, column=0)
user_id_entry = Entry(width=25)
user_id_entry.grid(row=2, column=1)

continue_button = Button(text="Tovább", command=continue_bt, padx=10)
continue_button.grid(row=4, column=1, padx=100, pady=20)

window.mainloop()
