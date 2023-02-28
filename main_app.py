from hw4 import *
from tkinter import *
# from plot_geo import *

# create python UI
master = Tk()
master.title = "Park Recommender"
master.geometry("600x600")

# variables
var0 = StringVar()
var1 = StringVar()
var2 = StringVar()
var3 = StringVar()
var4 = StringVar()
var0.set("1")
var1.set("2")
var2.set("3")
var3.set("4")
var4.set("5")
# var5 = StringVar()

bool0 = IntVar()
bool1 = IntVar()
bool2 = IntVar()
bool3 = IntVar()
bool4 = IntVar()
# bool5 = IntVar()

bool0.set(1)
bool1.set(1)
bool2.set(1)
bool3.set(1)
bool4.set(1)
# bool5.set(1)

label0 = Label(master, text='Distance', font=('calibre', 10, 'bold'))
label1 = Label(master, text='Temperature', font=('calibre', 10, 'bold'))
label2 = Label(master, text='Weather', font=('calibre', 10, 'bold'))
label3 = Label(master, text='Wind Speed', font=('calibre', 10, 'bold'))
label4 = Label(master, text='Rating', font=('calibre', 10, 'bold'))
# label5 = Label(master, text='Crime Rate', font=('calibre', 10, 'bold'))

entry0 = Entry(master, textvariable=var0, font=('calibre', 10, 'normal'))
entry1 = Entry(master, textvariable=var1, font=('calibre', 10, 'normal'))
entry2 = Entry(master, textvariable=var2, font=('calibre', 10, 'normal'))
entry3 = Entry(master, textvariable=var3, font=('calibre', 10, 'normal'))
entry4 = Entry(master, textvariable=var4, font=('calibre', 10, 'normal'))
# entry5 = Entry(master, textvariable=var5, font=('calibre', 10, 'normal'))

btn0 = Checkbutton(master, variable=bool0)
btn1 = Checkbutton(master, variable=bool1)
btn2 = Checkbutton(master, variable=bool2)
btn3 = Checkbutton(master, variable=bool3)
btn4 = Checkbutton(master, variable=bool4)
# btn5 = Checkbutton(master, variable=bool5)


def add_preference_data(data, name, is_active, rank):
    data[name] = {"is_active": is_active, "rank": int(rank)}
    return


def get_preference():
    data = {}
    add_preference_data(data, "distance", bool0.get(), var0.get())
    add_preference_data(data, "temperature", bool1.get(), var1.get())
    add_preference_data(data, "weather", bool2.get(), var2.get())
    add_preference_data(data, "windspeed", bool3.get(), var3.get())
    add_preference_data(data, "rating", bool4.get(), var4.get())
    return data


def submit():
    park_location_data = read_all_park_location_data()
    display_objects_info(park_location_data)
    cur_lat = DEFAULT_LAT
    cur_long = DEFAULT_LONG
    if lat_var.get() != "" and lat_var.get()[-1].isdigit() and long_var.get() != "" and long_var.get()[-1].isdigit():
        cur_lat = float(lat_var.get())
        cur_long = float(long_var.get())
    nearest_parks = get_nearest_parks(park_location_data, cur_lat, cur_long)
    weather_data = get_all_weather_info(nearest_parks)
    display_objects_info(weather_data)
    #
    rating_data = get_all_rating_info(nearest_parks)
    display_objects_info(rating_data)

    pref = get_preference()
    result = get_rank(
        preference=pref, distance_data=nearest_parks, weather_data=weather_data, rating_data=rating_data)
    print("\nRecommended Parks: ")
    display_objects_info(result)
    res_txt = ""
    latlst = []
    lonlst = []
    namelst = []
    for i in range(5):
        data = result[i]
        latlst.append(float(data["lat"]))
        lonlst.append(float(data["long"]))
        namelst.append(data["name"])
        res_txt += data["name"] + "\n"
    res_str.set(res_txt)
    # print("\nPlotting Parks:")
    # plot_on_map(float(cur_lat), float(cur_long), latlst, lonlst, namelst)


# btn will call submit
sub_btn = Button(master, text='Recommend Parks', command=submit)

labelcol = 1
label0.grid(row=0,column=labelcol,sticky=W)
label1.grid(row=1,column=labelcol,sticky=W)
label2.grid(row=2,column=labelcol,sticky=W)
label3.grid(row=3,column=labelcol,sticky=W)
label4.grid(row=4,column=labelcol,sticky=W)

entrycol = 2
entry0.grid(row=0,column=entrycol)
entry1.grid(row=1,column=entrycol)
entry2.grid(row=2,column=entrycol)
entry3.grid(row=3,column=entrycol)
entry4.grid(row=4,column=entrycol)

btncol = 0
btn0.grid(row=0,column=btncol)
btn1.grid(row=1,column=btncol)
btn2.grid(row=2,column=btncol)
btn3.grid(row=3,column=btncol)
btn4.grid(row=4,column=btncol)

tooltip_start = 6

label_tooltip0 = Label(master, text="Uncheck the box if you don't care about this factor", font=('calibre', 10, 'bold'))
label_tooltip1 = Label(master, text='Rank all factors from 1 to 5, 1 is the highest', font=('calibre', 10, 'bold'))

label_tooltip0.grid(row=tooltip_start,columnspan=3,sticky=W)
label_tooltip1.grid(row=tooltip_start+1,columnspan=3,sticky=W)

lat_var=StringVar()
long_var=StringVar()
lat_var.set("Enter your latitude.")
long_var.set("Enter your longitude.")
lat_entry = Entry(master, textvariable=lat_var, font=('calibre', 10, 'normal'))
long_entry = Entry(master, textvariable=long_var, font=('calibre', 10, 'normal'))
lat_entry.grid(row=tooltip_start+4,columnspan=5,sticky=W)
long_entry.grid(row=tooltip_start+5,columnspan=5,sticky=W)
master.grid_rowconfigure(tooltip_start+3, minsize=20)  # Here

label_tooltip3 = Label(master, text="If you don't provide lat or long, the location of USC will be used.", font=('calibre', 10, 'bold'))
label_tooltip3.grid(row=tooltip_start+6,columnspan=3,sticky=W)

master.grid_rowconfigure(tooltip_start+7, minsize=20)  # Here
sub_btn.grid(row=tooltip_start+8,columnspan=1, sticky=W)

master.grid_rowconfigure(tooltip_start+9, minsize=20)  # Here

res_str = StringVar()
res_str.set("")
label_result = Label(master, textvariable=res_str, font=('calibre', 10, 'bold'))
label_result.grid(row=tooltip_start+10,sticky=W)


mainloop()