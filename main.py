# group 7 app - price tracker

from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import random
import sqlite3
import string


conn = sqlite3.connect("price_tracker.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS STORE("
          "     store_code VARCHAR(10) NOT NULL,"
          "     store_name	VARCHAR(30) NOT NULL,"
          "     store_add	VARCHAR(150) NOT NULL,"
          "     PRIMARY KEY(store_code)"
          ")")
c.execute("CREATE TABLE IF NOT EXISTS PRODUCTS("
          "     prod_code VARCHAR(10) NOT NULL,"
          "     prodd_name VARCHAR(30) NOT NULL, "
          "     PRIMARY KEY(prod_code)"
          ")")
c.execute("CREATE TABLE IF NOT EXISTS PRODUCT_PRICE("
          "     store_code	VARCHAR(10) NOT NULL,"
          "     prod_code	VARCHAR(10) NOT NULL,"
          "     price DOUBLE NOT NULL,"
          "     date_modified DATE NOT NULL,"
          "     PRIMARY KEY(store_code, prod_code, date_modified),"
          "     FOREIGN KEY (store_code) REFERENCES STORE(store_code)"
          "         ON UPDATE CASCADE"
          "         ON DELETE CASCADE,"
          "     FOREIGN KEY (prod_code) REFERENCES PRODUCTS(prod_code)"
          "         ON UPDATE CASCADE"
          "         ON DELETE CASCADE"
          ")")
c.execute("CREATE TABLE IF NOT EXISTS PROD_CATEGORY("
          "     prod_code	VARCHAR(10) NOT NULL,"
          "     prod_categ VARCHAR(20) NOT NULL,"
          "     FOREIGN KEY (prod_code) REFERENCES PRODUCTS(prod_code)"
          "         ON DELETE CASCADE,"
          "     PRIMARY KEY (prod_code, prod_categ)"
          ")")


def exit_app(app):
    if messagebox.askyesno("Exit", "Do you want to exit?"):
        app.destroy()
    else:
        return


def prod_view(pid, sid):
    def display_price_history():
        f_dph = Toplevel()
        f_dph.title("Price History of " + pname)
        dphw = 350
        dphh = 290
        f_dph.config(bg="white")
        f_dph.resizable(False, False)
        f_dph.geometry("{}x{}+{}+{}".format(dphw, dphh, int((scw - dphw) / 2), int((scy - 60 - dphh) / 2)))
        f_dph.grab_set()
        f_dph.iconbitmap(r"images\icon.ico")

        f_table = Frame(f_dph)
        f_table.place(x=0, y=0, height=dphh, width=dphw)
        t_ph = ttk.Treeview(f_table, columns=("price", "date"))
        dphy = Scrollbar(f_table, orient=VERTICAL, command=t_ph.yview)
        dphy.pack(side=RIGHT, fill=Y)
        t_ph.configure(yscrollcommand=dphy.set)
        t_ph.heading("price", text="PRICE")
        t_ph.heading("date", text="DATE MODIFIED")
        t_ph['show'] = 'headings'
        t_ph.column("price", width=100, anchor="center")
        t_ph.column("date", width=240, anchor='center')
        t_ph.pack(fill=BOTH, expand=1)

        bg = ttk.Style()
        bg.theme_use("clam")
        bg.configure('Treeview', bd=2)
        bg.configure('Treeview.Heading', background="#1db954", foreground="black", font=("Roboto", 12, "bold"), bd=2)

        c.execute("SELECT price, date_modified FROM PRODUCT_PRICE WHERE store_code=? AND prod_code=?", (sid, pid))
        ph = c.fetchall()
        t_ph.delete(*t_ph.get_children())
        for hp in ph:
            date = datetime.strptime(hp[1], '%Y-%m-%d %H:%M:%S')
            t_ph.insert('', 0, values=(("Php " + '{:,.2f}'.format(round(hp[0], 2))),
                                       date.strftime('%I:%M %p - %a, %b %d %Y')))

    c.execute("SELECT prodd_name FROM PRODUCTS WHERE prod_code=?", (pid,))
    pname = c.fetchone()[0]
    f_prod = Toplevel()
    f_prod.title("Product Details of " + pname)
    psw = 420
    psh = 300
    f_prod.geometry("{}x{}+{}+{}".format(psw, psh, int((scw - psw) / 2), int((scy - 60 - psh) / 2)))
    f_prod.resizable(False, False)
    f_prod.grab_set()
    f_prod.config(bg="#0c0c0c")
    f_prod.iconbitmap(r"images\icon.ico")

    i_name = PhotoImage(file=r"images/spprod.png").subsample(2, 2)
    i_categ = PhotoImage(file=r"images/spcateg.png").subsample(2, 2)
    i_price = PhotoImage(file=r"images/spprice.png").subsample(2, 2)
    i_sname = PhotoImage(file=r"images/spstore.png").subsample(2, 2)
    i_sloc = PhotoImage(file=r"images/sploc.png").subsample(2, 2)

    name = Label(f_prod, text=("    " + pname), font=("Roboto", 13, "bold"), fg="#1db954", bg="#0c0c0c",
                 image=i_name, anchor="sw", compound="left")
    name.img = i_name
    name.place(x=10, y=30, height=40)
    pcateg = categ_prod(pid)
    categ = Label(f_prod, text=("    " + ", ".join(str(x.strip()) for x in pcateg)), font=("Roboto", 10, "bold"),
                  fg="white", bg="#0c0c0c", image=i_categ, anchor="sw", compound="left")
    categ.img = i_categ
    categ.place(x=10, y=75, height=40)
    c.execute("SELECT price, MAX(date_modified) AS date_modified FROM PRODUCT_PRICE WHERE prod_code=? AND "
              "store_code=?", (pid, sid))
    price = Label(f_prod, text=("    Php " + '{:,.2f}'.format(round(c.fetchone()[0], 2))), compound="left",
                  font=("Roboto", 12, "bold"), fg="#EC9D46", bg="#0c0c0c", image=i_price, anchor="sw")
    price.img = i_price
    price.place(x=10, y=120, height=40)
    c.execute("SELECT * FROM STORE WHERE store_code=?", (sid,))
    st = c.fetchone()
    store = Label(f_prod, text=("    " + st[1]), font=("Roboto", 12, "bold"), fg="#CF97A2", bg="#0c0c0c",
                  image=i_sname, anchor="sw", compound="left")
    store.img = i_sname
    store.place(x=10, y=165, height=40)
    loc = Label(f_prod, text=("    " + st[2]), font=("Roboto", 12, "bold"), fg="#1db954", bg="#0c0c0c", image=i_sloc,
                anchor="sw", compound="left")
    loc.img = i_sloc
    loc.place(x=10, y=210, height=40)
    Button(f_prod, text="View Price History", font=("Roboto", 10, "bold"), command=display_price_history,
           fg="black", bg="#1db954", activebackground="black", activeforeground="white")\
        .place(x=260, y=265, height=25, width=150)


def categ_prod(pid):
    pcateg = []
    c.execute("SELECT prod_categ FROM PROD_CATEGORY WHERE prod_code=?", (pid,))
    sp_categ = c.fetchall()
    for ct in sp_categ:
        pcateg.append(ct[0])
    return pcateg


class Tracker:
    def __init__(self, frame):
        self.f_home = Frame(frame, bg="#0C0C0C")
        self.f_store = Frame(frame, bg="white")
        self.f_search = Frame(frame, bg="#D9D6D8")

        self.prod_search = StringVar()
        self.store_search = StringVar()
        self.vp_search = StringVar()

        self.store_search.trace("w", lambda name, index, mode, sv=self.store_search: self.display_store())

        self.s_name = StringVar()

        self.p_name = StringVar()
        self.p_price = DoubleVar()

        f_nav = Frame(frame, bg="#1DB954")
        f_nav.place(x=0, y=0, height=40, width=480)

        home_img = PhotoImage(file=r"images/home.png")
        store_img = PhotoImage(file=r"images/store.png")
        prod_img = PhotoImage(file=r"images/product.png")
        bsearch_img = PhotoImage(file=r"images/blacksearch.png")
        self.loc_img = PhotoImage(file=r"images/loc.png").subsample(2, 2)

        self.homebtn = Button(f_nav, command=self.home, relief=FLAT, image=home_img, anchor="center",
                              bg="#1DB954", activebackground="#1DB954")
        self.homebtn.img = home_img
        self.e_search_prod = Entry(f_nav, textvariable=self.prod_search, font=("Roboto", 12))
        self.e_search_prod.bind('<Return>', lambda event: self.search_product())
        self.b_search_prod = Button(f_nav, command=lambda: self.search_product, image=bsearch_img, anchor="center",
                                    bg="#1DB954", activebackground="#1DB954", relief=FLAT)
        self.b_search_prod.img = bsearch_img

        storebtn = Button(f_nav, command=self.store, relief=FLAT, image=store_img, anchor="center",
                          bg="#1DB954", activebackground="#1DB954")
        storebtn.img = store_img
        storebtn.place(x=400, y=0, height=40, width=40)
        prodbtn = Button(f_nav, command=self.add_product, relief=FLAT, image=prod_img, anchor="center",
                         bg="#1DB954", activebackground="#1DB954")
        prodbtn.img = prod_img
        prodbtn.place(x=440, y=0, height=40, width=40)

        self.home()

    def hide(self):
        self.homebtn.place_forget()
        self.e_search_prod.place_forget()
        self.b_search_prod.place_forget()
        self.f_home.place_forget()
        self.f_store.place_forget()
        self.f_search.place_forget()

    def home(self):
        self.hide()
        self.prod_search.set("Enter product name:")
        self.f_home.place(x=0, y=40, height=640, width=480)
        gsearch_img = PhotoImage(file=r"images/search.png")
        banner_img = PhotoImage(file=r"images/banner.png")
        banner = Label(self.f_home, image=banner_img)
        banner.img = banner_img
        banner.place(x=50, y=120, height=200, width=380)
        e_prod = Entry(self.f_home, textvariable=self.prod_search, font=("Roboto", 15))
        e_prod.bind('<FocusIn>', lambda event: self.prod_search.set(""))
        e_prod.bind('<Return>', lambda event: self.search_frame())
        e_prod.place(x=50, y=340, height=40, width=380)
        b_srch = Button(self.f_home, relief=FLAT, command=lambda: self.search_frame(), image=gsearch_img,
                        anchor="center", bg="#1DB954", activebackground="#1DB954")
        b_srch.img = gsearch_img
        b_srch.place(x=388, y=342, width=40, height=36)

    # SEARCH PRODUCT METHODS

    def search_frame(self):
        if self.prod_search.get() == "" or self.prod_search.get() == "Enter product name:":
            return
        self.homebtn.place(x=0, y=0, width=40, height=40)
        self.e_search_prod.place(x=50, y=5, height=30, width=250)
        self.b_search_prod.place(x=300, y=5, height=30, width=35)
        self.search_product()

    def search_product(self):
        if self.prod_search.get() == "" or self.prod_search.get() == "Enter product name:":
            return
        self.f_search.place(x=10, y=70, height=620, width=460)
        f_rsearch = Frame(self.f_search)
        c_search_res = Canvas(f_rsearch, width=440, height=550)
        f_rsearch.place(x=5, y=40, width=450, height=560)
        res_frame = Frame(c_search_res)
        rsy = Scrollbar(f_rsearch, orient=VERTICAL, command=c_search_res.yview)
        rsy.pack(side=RIGHT, fill=Y)
        c_search_res.pack(side=LEFT)
        c_search_res.configure(yscrollcommand=rsy.set)
        c_search_res.bind('<Configure>', lambda e: c_search_res.configure(scrollregion=c_search_res.bbox('all')))
        c_search_res.create_window((0, 0), window=res_frame, anchor="nw")

        Label(self.f_search, text="Search Results for: ", font=("Roboto", 12, "bold"), bg="#D9D6D8", anchor="sw"). \
            place(x=5, y=0, height=35, width=150)
        Label(self.f_search, text=self.prod_search.get(), font=("Roboto", 12, "bold"), bg="#D9D6D8",
              fg="#1DB954", anchor="sw").place(x=155, y=0, height=35, width=290)

        c.execute("SELECT prod_code FROM PRODUCTS WHERE prodd_name LIKE ?", ('%' + self.prod_search.get() + '%',))
        prods = c.fetchall()
        for frame in res_frame.winfo_children():
            frame.destroy()
        count = 0
        row = 0

        if not prods:
            nopfr = Frame(res_frame, width=450, height=540)
            nopfr.propagate(0)
            nopfr.grid(row=0, column=0)
            Label(nopfr, text="No Results", font=("Gotham Medium", 24, "bold"), fg="#1DB954") \
                .place(x=0, y=0, height=440, width=430)
        else:
            for prod in prods:
                try:
                    c.execute("SELECT price, MAX(date_modified) AS date_modified, store_code FROM PRODUCT_PRICE "
                              "WHERE prod_code=? GROUP BY store_code", (prod[0],))
                    pr = c.fetchall()
                    for p in pr:
                        if count > 0 and count % 2 == 0:
                            row += 1
                        f_pd = Frame(res_frame, highlightthickness=1, height=150, width=210, bg="white",
                                     highlightbackground="#1db954")
                        f_pd.propagate(0)
                        pprice = Label(f_pd, text=("Php " + '{:,.2f}'.format(round(p[0], 2))), anchor="sw",
                                       font=("Roboto", 10, "bold"), bg="white", fg="orange")
                        pprice.place(x=15, y=65, height=40, width=180)
                        f_pd.grid(row=row, column=count % 2, padx=3, pady=(5, 0))
                        c.execute("SELECT prodd_name FROM PRODUCTS WHERE prod_code=?", (prod[0],))
                        name = c.fetchone()[0]
                        pname = Label(f_pd, text=name, font=("Roboto", 14, "bold"), bg="white", anchor="nw")
                        pname.place(x=5, y=20, height=30, width=190)
                        c.execute("SELECT store_name FROM STORE WHERE store_code=?", (p[2],))
                        det_store = c.fetchone()
                        store = Label(f_pd, image=self.loc_img, text=(" " + det_store[0]), font=("Roboto", 8, "bold"),
                                      bg="white", anchor="se", compound="left")
                        store.img = self.loc_img
                        store.place(x=5, y=125, height=20, width=190)
                        f_pd.bind('<Double-1>', lambda event, a=prod[0], b=p[2]: prod_view(a, b))
                        pname.bind('<Double-1>', lambda event, a=prod[0], b=p[2]: prod_view(a, b))
                        pprice.bind('<Double-1>', lambda event, a=prod[0], b=p[2]: prod_view(a, b))
                        store.bind('<Double-1>', lambda event, a=prod[0], b=p[2]: prod_view(a, b))
                        count += 1
                except TypeError:
                    continue
            if count == 0:
                nores = Frame(res_frame)
                nores.configure(width=450, height=540)
                nores.propagate(0)
                nores.grid(row=0, column=0)
                Label(nores, text="No Results", font=("Gotham Medium", 24, "bold"), fg="#1DB954") \
                    .place(x=0, y=0, height=440, width=430)

    # STORE INTERFACE METHODS

    def store(self):
        self.hide()
        self.homebtn.place(x=0, y=0, width=40, height=40)
        self.f_store.place(x=10, y=60, height=610, width=460)
        gsearch_img = PhotoImage(file=r"images/search.png")

        Label(self.f_store, text="Stores", font=("Gotham Medium", 25, "bold"), bg="white").place(x=10, y=5, height=40)
        Button(self.f_store, text="ADD STORE", font=("Roboto", 10, "bold"), command=self.add_store_frame, relief=GROOVE,
               fg="black", activeforeground="black", bg="#1DB954", activebackground="#1DB954").\
            place(x=360, y=15, height=25, width=90)
        Entry(self.f_store, font=("Roboto", 11, "bold"), highlightbackground="#1DB954",
              textvariable=self.store_search, highlightcolor="#1DB954", highlightthickness=2)\
            .place(x=170, y=70, height=30, width=250)
        s = Label(self.f_store, image=gsearch_img, bg="#1db954")
        s.img = gsearch_img
        s.place(x=420, y=70, height=30, width=30)
        self.display_store()

    def add_store_frame(self):
        f_addstore = Toplevel()
        f_addstore.title("Add Store")
        asw = 420
        ash = 350
        self.s_name.set("Enter store name")
        f_addstore.resizable(False, False)
        f_addstore.config(bg="#0c0c0c")
        f_addstore.geometry("{}x{}+{}+{}".format(asw, ash, int((scw - asw) / 2), int((scy - 60 - ash) / 2)))
        f_addstore.grab_set()
        f_addstore.iconbitmap(r"images\icon.ico")

        Label(f_addstore, text="ADD STORE", font=("Gotham Medium", 20, "bold"), anchor="center",
              fg="#1DB954", bg="#0C0C0C").\
            place(x=5, y=15, height=35, width=410)
        Label(f_addstore, text="NAME: ", font=("Gotham Medium", 13, "bold"), anchor="center",
              bg="#1DB954", fg="#0C0C0C").place(x=10, y=80, height=25)
        e_sname = Entry(f_addstore, textvariable=self.s_name, font=("Roboto", 11, "bold"))
        e_sname.bind('<FocusIn>', lambda event: self.st_focusin())
        e_sname.bind('<FocusOut>', lambda event: self.st_focusout())
        e_sname.place(x=10, y=115, height=25, width=400)
        Label(f_addstore, text="ADDRESS:", font=("Gotham Medium", 13, "bold"), anchor="center",
              bg="#1DB954", fg="#0C0C0C").place(x=10, y=155, height=25)
        t_sadd = Text(f_addstore, font=("Roboto", 11, "bold"))
        t_sadd.place(x=10, y=190, height=100, width=400)
        t_sadd.insert(END, "Enter store address")
        t_sadd.bind('<FocusIn>', lambda event, y=t_sadd.get(1.0, END).replace("\n", ""):
                    t_sadd.delete(1.0, END) if y == "Enter store address" else "")
        t_sadd.bind('<FocusOut>', lambda event, y=t_sadd.get(1.0, END).replace("\n", ""):
                    t_sadd.insert(END, "Enter store address") if y == "" else "")

        Button(f_addstore, text="CONFIRM", font=("Roboto", 12, "bold"),
               command=lambda: self.add_store(t_sadd.get(1.0, END).replace("\n", ""), f_addstore))\
            .place(x=220, y=310, height=25, width=90)
        Button(f_addstore, text="CLEAR", font=("Roboto", 12, "bold"),
               command=lambda: [t_sadd.delete(1.0, END), self.s_name.set("Enter store name"),
                                t_sadd.insert(END, "Enter store address")])\
            .place(x=320, y=310, height=25, width=90)

    def add_store(self, add, frame):
        if self.s_name.get() == "" or self.s_name.get() == "Enter store name:" or add == "":
            messagebox.showerror("Error", "Please fill out all the necessary information.")
        else:
            if messagebox.askyesno("Add Store", "Confirm adding store?"):
                c.execute("INSERT INTO STORE VALUES(?, ?, ?)",
                          (''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),
                           self.s_name.get(), add))
                conn.commit()
                messagebox.showinfo("Success", "Store added to database!")
                frame.destroy()
                self.display_store()

    # METHOD FOR LIST OF STORES

    def display_store(self):
        d_store = Frame(self.f_store)
        c_stores = Canvas(d_store, width=440, height=480)
        f_store = Frame(c_stores)
        sy = Scrollbar(d_store, command=c_stores.yview, orient=VERTICAL)

        d_store.place(x=5, y=110, width=450, height=490)
        c_stores.configure(yscrollcommand=sy.set)
        sy.pack(side=RIGHT, fill=Y)
        c_stores.pack(side=LEFT)
        c_stores.bind('<Configure>', lambda e: c_stores.configure(scrollregion=c_stores.bbox('all')))
        c_stores.create_window((0, 0), window=f_store, anchor="nw")

        if self.store_search.get() == "":
            c.execute("SELECT * FROM STORE")
        else:
            c.execute("SELECT * FROM STORE WHERE Store_Name LIKE ?", ('%' + self.store_search.get() + '%',))
        stores = c.fetchall()
        for frame in f_store.winfo_children():
            frame.destroy()
        row = 0
        if not stores:
            nosfr = Frame(f_store, highlightthickness=1, height=480, width=430)
            nosfr.propagate(0)
            nosfr.grid(row=0, column=0)
            Label(nosfr, text="No Stores", font=("Gotham Medium", 24, "bold"), fg="#1DB954")\
                .place(x=0, y=0, height=480, width=430)
        else:
            for store in stores:
                s_frame = Frame(f_store, highlightthickness=1, height=95, width=430, bg="white")
                s_frame.propagate(0)
                s_frame.grid(row=row, column=0, pady=(5, 0))
                Label(s_frame, text=store[1], font=("Roboto", 17, "bold"), bg="white", anchor="sw").\
                    place(x=10, y=5, height=50)
                loc = Label(s_frame, text=(" " + store[2]), font=("Roboto", 10, "bold"), bg="white", anchor="nw",
                            image=self.loc_img, compound="left", fg="#1db954")
                loc.img = self.loc_img
                loc.place(x=5, y=65, height=20)
                Button(s_frame, text="SET PRICES", font=("Roboto", 8, "bold"), relief=GROOVE,
                       fg="black", activeforeground="black", bg="#1DB954", activebackground="#1DB954",
                       command=lambda x=store[0]: self.view_prod_frame(x)).place(x=325, y=5, width=100, height=25)
                Button(s_frame, text="UPDATE DETAILS", font=("Roboto", 8, "bold"), relief=GROOVE,
                       fg="black", activeforeground="black", bg="#1DB954", activebackground="#1DB954",
                       command=lambda x=store[0]: self.f_up_store(x)).place(x=325, y=35, width=100, height=25)
                Button(s_frame, text="DELETE STORE", font=("Roboto", 8, "bold"), relief=GROOVE,
                       fg="black", activeforeground="black", bg="#1DB954", activebackground="#1DB954",
                       command=lambda x=store[0]: self.delete_store(x)).place(x=325, y=65, width=100, height=25)
                row += 1

    # METHODS FOR SET PRICES BUTTON

    def view_prod_frame(self, sid):
        f_view = Toplevel()
        f_view.title("Products")
        vpw = 450
        vph = 600
        f_view.resizable(False, False)
        f_view.config(bg="#1db954")
        f_view.geometry("{}x{}+{}+{}".format(vpw, vph, int((scw - vpw) / 2), int((scy - 60 - vph) / 2)))
        f_view.grab_set()
        f_view.iconbitmap(r"images\icon.ico")

        bsearch_img = PhotoImage(file=r"images/blacksearch.png")
        Entry(f_view, textvariable=self.vp_search, font=("Roboto", 14, "bold"), highlightcolor="black")\
            .place(x=10, y=15, width=400, height=30)
        search = Label(f_view, image=bsearch_img, bg="black", anchor="center")
        search.img = bsearch_img
        search.place(x=410, y=15, width=30, height=30)
        self.vp_search.trace("w", lambda name, index, mode, sv=self.vp_search: self.show_prod(f_view, sid))
        self.show_prod(f_view, sid)

    def show_prod(self, f, sid):
        f_vp = Frame(f)
        f_vp.place(x=5, y=70, width=440, height=525)
        c_vp = Canvas(f_vp, width=430, height=520)
        c_vp.place(x=0, y=0)
        rsy = Scrollbar(f_vp, orient=VERTICAL, command=c_vp.yview)
        rsy.pack(side=RIGHT, fill=Y)
        c_vp.configure(yscrollcommand=rsy.set)
        c_vp.pack(side=LEFT)
        fr_vp = Frame(c_vp)
        c_vp.bind('<Configure>', lambda e: c_vp.configure(scrollregion=c_vp.bbox('all')))
        c_vp.create_window((0, 0), window=fr_vp, anchor="nw")

        if self.vp_search.get() == "":
            c.execute("SELECT * FROM PRODUCTS")
        else:
            c.execute("SELECT * FROM PRODUCTS WHERE prodd_name LIKE ?", ('%' + self.vp_search.get() + '%',))
        prods = c.fetchall()
        row = 0

        if not prods:
            nospfr = Frame(fr_vp, bg="white", width=430, height=520)
            nospfr.propagate(0)
            nospfr.grid(row=0, column=0)
            Label(nospfr, text="No Products", font=('Roboto', 30, 'bold'), fg="#1db954", bg="white").\
                place(x=0, y=0, width=430, height=520)
        else:
            for pr in prods:
                f_sp = Frame(fr_vp, highlightthickness=1, height=120, width=410, bg="white",
                             highlightbackground="#1db954")
                f_sp.propagate(0)
                f_sp.grid(row=row, column=0, padx=5, pady=(5, 0))
                Label(f_sp, text=pr[1], anchor='w', font=("Roboto", 17, "bold"), bg="white")\
                    .place(x=10, y=10, height=50, width=285)
                sp_categ = categ_prod(pr[0])
                Label(f_sp, text=", ".join(str(x.strip()) for x in sp_categ), anchor='sw',
                      font=("Roboto", 9, "bold"), bg="white", fg="#1db954").place(x=10, y=60, height=20, width=285)

                Button(f_sp, text="Update Details", font=("Roboto", 9, "bold"), bg="#1db954", relief=GROOVE,
                       activebackground="#1db954", command=lambda x=pr[0], y=f, z=sid: self.f_up_details(x, y, z))\
                    .place(x=304, y=6, height=32, width=100)
                Button(f_sp, text="Update Price", font=("Roboto", 9, "bold"), bg="#1db954", relief=GROOVE,
                       activebackground="#1db954", command=lambda x=pr[0], y=f, z=sid: self.f_up_price(x, y, z))\
                    .place(x=304, y=44, height=32, width=100)
                Button(f_sp, text="Delete Product", font=("Roboto", 9, "bold"), bg="#1db954", relief=GROOVE,
                       activebackground="#1db954", command=lambda x=pr[0], y=f, z=sid: self.delete_prod(x, y, z))\
                    .place(x=304, y=82, height=32, width=100)

                row += 1

    # METHOD FOR UPDATE PRODUCT DETAILS BUTTON

    def f_up_details(self, pid, f, sid):
        c.execute("SELECT prodd_name FROM PRODUCTS WHERE prod_code=?", (pid,))
        name = c.fetchone()[0]
        f_up_de = Toplevel()
        f_up_de.title("Update Details of " + name)
        udew = 400
        udeh = 280
        f_up_de.config(bg="#1db954")
        f_up_de.geometry("{}x{}+{}+{}".format(udew, udeh, int((scw - udew) / 2), int((scy - 60 - udeh) / 2)))
        f_up_de.resizable(False, False)
        f_up_de.grab_set()
        f_up_de.iconbitmap(r"images\icon.ico")

        self.p_name.set(name)
        c.execute("SELECT prod_categ FROM PROD_CATEGORY WHERE prod_code=?", (pid,))
        cts = c.fetchall()

        Label(f_up_de, text="NAME: ", font=("Gotham Medium", 12, "bold"), anchor="center", fg="#1DB954",
              bg="#0C0C0C").place(x=10, y=30, height=25, width=80)
        pdname = Entry(f_up_de, textvariable=self.p_name, font=("Roboto", 11, "bold"), highlightcolor="#1DB954",
                       highlightbackground="#1DB954")
        pdname.place(x=90, y=30, height=25, width=300)
        Label(f_up_de, text="CATEGORY: ", font=("Gotham Medium", 12, "bold"), anchor="center", fg="#1DB954",
              bg="#0C0C0C").place(x=10, y=65, height=25)
        Label(f_up_de, text="(Please separate each category using comma)", font=("Roboto", 8, "bold"), bg="#1db954",
              fg="#0c0c0c", anchor="center").place(x=125, y=65, height=25)
        pdcateg = Text(f_up_de, font=("Roboto", 11, "bold"))
        pdcateg.place(x=10, y=95, height=120, width=380)
        pdcateg.insert(END, ", ".join(str(x[0].strip()) for x in cts))

        Button(f_up_de, text="CONFIRM", font=("Roboto", 12, "bold"),
               command=lambda: self.update_details(pid, f, sid, f_up_de, pdcateg.get(1.0, END).replace("\n", ""))) \
            .place(x=310, y=230, width=80, height=30)

    def update_details(self, pid, f, sid, top, ctgs):
        c.execute("SELECT prodd_name FROM PRODUCTS WHERE prod_code=?", (pid,))
        name = c.fetchone()[0]
        if ctgs == "" or self.p_name.get() == "":
            messagebox.showerror("Error", "Please fill out all the necessary information!")
        else:
            ctgs = ctgs.split(",")
            if messagebox.askyesno("Update Product Details", ("Do you want to update the details of " + name)):
                c.execute("DELETE FROM PROD_CATEGORY WHERE prod_code=?", (pid,))
                conn.commit()
                c.execute("UPDATE PRODUCTS SET prodd_name=? WHERE prod_code=?", (self.p_name.get(), pid))
                for ctg in ctgs:
                    c.execute("INSERT INTO PROD_CATEGORY VALUES(?, ?)", (pid, ctg.strip()))
                conn.commit()
                self.pd_focusout()
                top.destroy()
                self.show_prod(f, sid)
                messagebox.showinfo("Success", ("Details of " + name + " has been updated!"))

    # METHOD FOR UPDATE PRICE BUTTON

    def f_up_price(self, pid, fr, stid):
        c.execute("SELECT prodd_name FROM PRODUCTS WHERE prod_code=?", (pid,))
        f_up_pr = Toplevel()
        f_up_pr.title("Update Price of " + c.fetchone()[0])
        uprw = 250
        uprh = 110
        f_up_pr.geometry("{}x{}+{}+{}".format(uprw, uprh, int((scw - uprw) / 2), int((scy - 60 - uprh) / 2)))
        f_up_pr.config(bg="#1db954")
        f_up_pr.resizable(False, False)
        f_up_pr.grab_set()
        f_up_pr.iconbitmap(r"images\icon.ico")

        Label(f_up_pr, text="PRICE: ", font=("Gotham Medium", 12, "bold"), anchor="center", fg="#1DB954",
              bg="#0C0C0C").place(x=10, y=20, height=25, width=80)
        pdprice = Entry(f_up_pr, textvariable=self.p_price, highlightcolor="#0C0C0C", highlightbackground="#0C0C0C",
                        font=("Roboto", 12, "bold"))
        pdprice.place(x=90, y=20, height=25, width=150)
        Button(f_up_pr, text="CONFIRM", font=("Roboto", 12, "bold"),
               command=lambda: self.update_price(pid, stid, fr, f_up_pr))\
            .place(x=160, y=70, width=80, height=30)

    def update_price(self, p, s, pf, top):
        c.execute("SELECT prodd_name FROM PRODUCTS WHERE prod_code=?", (p,))
        name = c.fetchone()[0]
        try:
            if self.p_price.get() > 0:
                if messagebox.askyesno("Update Price", "Are you sure you want to update the price?"):
                    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    c.execute("INSERT INTO PRODUCT_PRICE VALUES(?, ?, ?, ?)",
                              (s, p, self.p_price.get(), date))
                    conn.commit()
                    self.p_price.set(0)
                    top.destroy()
                    self.show_prod(pf, s)
                    messagebox.showinfo("Success", ("Price of " + name + " has been updated"))
                    return
            else:
                messagebox.showerror("Error", "Please input valid price.")
        except TclError:
            messagebox.showerror("Error", "Please input valid price.")

    # METHOD FOR DELETE PRODUCT BUTTON

    def delete_prod(self, pid, f, sid):
        if messagebox.askyesno("Delete Product", "Confirm deleting product?"):
            c.execute("DELETE FROM PRODUCTS WHERE prod_code=?", (pid,))
            c.execute("DELETE FROM PRODUCT_PRICE WHERE prod_code=?", (pid,))
            c.execute("DELETE FROM PROD_CATEGORY WHERE prod_code=?", (pid,))
            conn.commit()
            self.show_prod(f, sid)
            messagebox.showinfo("Success", "Product deleted in database.")

    # METHOD FOR UPDATE STORE DETAILS

    def f_up_store(self, sid):
        c.execute("SELECT store_name, store_add FROM STORE WHERE store_code=?", (sid,))
        store = c.fetchone()
        usw = 420
        ush = 350
        f_ups = Toplevel()
        f_ups.title("Update Store Details of " + store[0])
        f_ups.geometry("{}x{}+{}+{}".format(usw, ush, int((scw - usw) / 2), int((scy - 60 - ush) / 2)))
        f_ups.grab_set()
        f_ups.resizable(False, False)
        f_ups.config(bg="#0c0c0c")
        f_ups.iconbitmap(r"images\icon.ico")
        self.s_name.set(store[0])

        Label(f_ups, text="UPDATE STORE", font=("Gotham Medium", 20, "bold"), anchor="center", fg="#1DB954",
              bg="#0C0C0C").place(x=5, y=15, height=35, width=410)
        Label(f_ups, text="NAME: ", font=("Gotham Medium", 13, "bold"), bg="#1DB954",
              anchor="center", fg="#0C0C0C").place(x=10, y=80, height=25)
        Entry(f_ups, font=("Roboto", 11, "bold"), textvariable=self.s_name).place(x=10, y=115, height=25, width=400)
        Label(f_ups, text="ADDRESS:", font=("Gotham Medium", 13, "bold"), bg="#1DB954", anchor="center", fg="#0C0C0C")\
            .place(x=10, y=155, height=25)
        t_sadd = Text(f_ups, font=("Roboto", 11, "bold"))
        t_sadd.insert(END, store[1])
        t_sadd.place(x=10, y=190, height=100, width=400)

        Button(f_ups, text="CONFIRM", font=("Roboto", 12, "bold"),
               command=lambda: self.update_store(sid, t_sadd.get(1.0, END).replace("\n", ""), f_ups)).\
            place(x=220, y=310, height=25, width=90)
        Button(f_ups, text="CLEAR", font=("Roboto", 12, "bold"),
               command=lambda: [t_sadd.delete(1.0, END), self.s_name.set("Enter store name"),
                                t_sadd.insert(END, "Enter store address")]) \
            .place(x=320, y=310, height=25, width=90)

    def update_store(self, sid, add, f):
        c.execute("SELECT store_name FROM STORE WHERE store_code=?", (sid,))
        name = c.fetchone()[0]
        if self.s_name.get() == "" or self.s_name.get() == "Enter store name:" or add == "":
            messagebox.showerror("Error", "Please fill out all the necessary information.")
        else:
            if messagebox.askyesno("Update Store Details", ("Do you want to update the store details of " +
                                                            name)):
                c.execute("UPDATE STORE SET store_name=?, store_add=? WHERE store_code=?",
                          (self.s_name.get(), add, sid))
                conn.commit()
                messagebox.showinfo("Success", ("Store details of " + name + " updated!"))
                f.destroy()
                self.display_store()

    # METHOD FOR DELETE STORE BUTTON

    def delete_store(self, storeid):
        if messagebox.askyesno("Delete Store", "Do you want to delete this store?"):
            c.execute("DELETE FROM STORE WHERE store_code=?", (storeid,))
            self.display_store()
            messagebox.showinfo("Success", "Store deleted from database!")
            conn.commit()

    # METHOD FOR PRODUCT BUTTON IN NAVIGATION

    def add_product(self):
        w_add_prod = Toplevel()
        w_add_prod.title("Add Product!")
        apw = 400
        aph = 330
        w_add_prod.config(bg="#0c0c0c")
        w_add_prod.geometry("{}x{}+{}+{}".format(apw, aph, int((scw - apw) / 2), int((scy - 60 - aph) / 2)))
        w_add_prod.resizable(False, False)
        w_add_prod.grab_set()
        w_add_prod.iconbitmap(r"images\icon.ico")
        self.p_name.set("Enter product name")

        Label(w_add_prod, text="Add Product", bg="#0C0C0C", fg="#1DB954", font=("Gotham Medium", 18, "bold")) \
            .place(x=5, y=15, height=35, width=410)
        Label(w_add_prod, text="Name: ", font=("Gotham Medium", 14, "bold"), anchor="center",
              bg="#1DB954", fg="#0C0C0C").place(x=10, y=85, height=25, width=80)
        pdname = Entry(w_add_prod, textvariable=self.p_name, highlightcolor="#1DB954",
                       highlightbackground="#1DB954",
                       font=("Roboto", 11, "bold"))
        pdname.bind('<FocusIn>', lambda event: self.pd_focusin())
        pdname.bind('<FocusOut>', lambda event: self.pd_focusout())
        pdname.place(x=90, y=85, height=25, width=300)
        Label(w_add_prod, text="Category: ", font=("Gotham Medium", 14, "bold"), anchor="center",
              bg="#1DB954", fg="#0C0C0C").place(x=10, y=125, height=25, width=120)
        Label(w_add_prod, text="(Please separate each category using comma)", font=("Roboto", 8), fg="#1db954",
              bg="#0c0c0c", anchor="center").place(x=135, y=120, height=25)
        pdcateg = Text(w_add_prod, font=("Roboto", 11, "bold"))
        pdcateg.place(x=10, y=150, height=120, width=380)

        pdcateg.insert(END, "Enter product category")
        pdcateg.bind('<FocusIn>', lambda event, y=pdcateg.get(1.0, END).replace("\n", ""): pdcateg.delete(1.0, END)
                     if y == "Enter product category" else "")

        Button(w_add_prod, text="CONFIRM", font=("Roboto", 12, "bold"),
               command=lambda: self.add_pd(pdcateg.get(1.0, END).replace("\n", ""), w_add_prod)) \
            .place(x=220, y=290, width=80, height=30)
        Button(w_add_prod, text="CLEAR", font=("Roboto", 12, "bold"),
               command=lambda: [self.p_name.set("Enter product name"), pdcateg.delete(1.0, END)]) \
            .place(x=310, y=290, width=80, height=30)

    def add_pd(self, categ, frame):
        if self.p_name.get() == "" or categ == "" or self.p_name.get() == "Enter product name":
            messagebox.showerror("Error", "Please provide all the necessary information!")
            return
        else:
            ctgs = categ.split(",")
            if messagebox.askyesno("Add Product", "Are you sure you want to add the product?"):
                try:
                    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                    c.execute("INSERT INTO PRODUCTS VALUES(?, ?)", (code, self.p_name.get()))
                    for ctg in ctgs:
                        c.execute("INSERT INTO PROD_CATEGORY VALUES(?, ?)", (code, ctg.strip()))
                    conn.commit()
                    messagebox.showinfo("Success", "Product added to database")
                    self.pd_focusout()
                    frame.destroy()
                    return
                except sqlite3.IntegrityError:
                    messagebox.showerror("Product code already in database!")

    # SOME EVENT LISTENERS

    def st_focusin(self):
        if self.s_name.get() == "Enter store name":
            self.s_name.set("")

    def st_focusout(self):
        if self.s_name.get() == "" or self.s_name.get() == "Enter store name":
            self.s_name.set("Enter store name")

    def pd_focusin(self):
        if self.p_name.get() == "Enter product name":
            self.p_name.set("")

    def pd_focusout(self):
        if self.p_name.get() == "" or self.p_name.get() == "Enter product name":
            self.p_name.set("Enter product name")


# STARTING CODE

root = Tk()
root.title("Price Tracker")
scw = root.winfo_screenwidth()
scy = root.winfo_screenheight()
w = 480
h = 680
root.geometry("{}x{}+{}+{}".format(w, h, int((scw - w) / 2), int((scy - 60 - h) / 2)))
root.resizable(False, False)
root.config(bg="#0C0C0C")
root.iconbitmap(r"images\icon.ico")
root.protocol("WM_DELETE_WINDOW", lambda: exit_app(root))
obj = Tracker(root)
root.mainloop()
