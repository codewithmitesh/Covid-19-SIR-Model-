from tkinter import *
from tkinter.messagebox import showinfo, askquestion, showerror
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import random, string
from tkinter import ttk
import smtplib as sp
from scipy.integrate import odeint
import numpy as np


def sir_graph():
    def enterValues():
        # Total population, population.
        population = int(sir_population.get())
        time_t = int(sir_days.get())
        # Initial number of infected and recovered individuals, i0 and r0.
        i0 = 1
        r0 = 0
        # Everyone else, s0, is susceptible to infection initially.
        s0 = population - i0 - r0
        # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
        beta = 0.2                        #   beta Is Infected Rate.
        gamma = 1./10                       # Gamma is Recovery Rate
        # A grid of time points (in days)
        t = np.linspace(0, time_t, time_t)           # to divide the 0 to time_t with respect to time_t.

        # The SIR model differential equations.
        def deriv(y, t, population, beta, gamma):                        
            s, i, r = y                                #to store the values of s , i ,r in to the tuple
            dSdt = -beta * s * i / population                
            dIdt = beta * s * i / population - gamma * i             
            dRdt = gamma * i
            return dSdt, dIdt, dRdt

        # Initial conditions vector
        y0 = s0, i0, r0
        # Integrate the SIR equations over the time grid, t.
        ret = odeint(deriv, y0, t, args=(population, beta, gamma))
        s, i, r = ret.T

        # Plot the data on three separate curves for s(t), i(t) and r(t)
        fig = plt.figure(facecolor='w')
        ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)     
        ax.plot(t, s / 1000, 'b', alpha=0.5, lw=2, label='Susceptible')       #ploting the graph it is Normal Graph
        ax.plot(t, i / 1000, 'r', alpha=0.5, lw=2, label='Infected')
        ax.plot(t, r / 1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
        ax.set_xlabel('Time /days')
        ax.set_ylabel(f'Number ({population}s)')
        ax.set_ylim(0, 1.2)
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        plt.show()

        quit_button = Button(text="Quit", bg="coral1", cursor="hand2", command = quit)
        canvas1.create_window(500, 390, window=quit_button)


    canvas1.create_text(190, 280, text="Population: ", fill="white", font=("Courier", 15, "bold"))
    population_value = IntVar()
    sir_population = Entry(root, textvariable=population_value)
    canvas1.create_window(325, 282, window=sir_population)

    canvas1.create_text(204, 303, text="No. of Days: : ", fill="white", font=("Courier", 15, "bold"))
    days_value = IntVar()
    sir_days = Entry(root, textvariable=days_value)
    canvas1.create_window(325, 302, window=sir_days)


    sir_input = Button(root, text='Enter', bg='coral1', cursor="hand2", command=enterValues)
    canvas1.create_window(320, 330, window=sir_input)


veri_code = ''.join(random.choices(string.ascii_letters + string.digits, k=4))   # random string for verification code


# ------ SENDING EMAIL -------
def send_email():   # defining the function
    email_id = emailvalue.get()  # getting the user input
    server = sp.SMTP_SSL("smtp.gmail.com", 465)                             # gmail hostname and server port
    server.login("demoemail621@gmail.com", "Demo@621")                      # senders email and pass
    message = 'Subject: {}\n\n{}'.format("Verification code for Covid-19 Analysis",
                                         f"Please enter this verification code: \n"
                                         f"{veri_code}")        # subject, body
    server.sendmail("demoemail621@gmail.com", f"{email_id}", f"{message}")  # sender's mail, receiver's mail, message
    server.quit()                                                           # terminate the process



# ------ CODE VERIFICATION ------
def verify_code():

    # ----- COMBOBOX SELECTIONS ------
    def select_value(event):            # select value function
        msg = f"You have selected {graph_menu.get()}."
        showinfo(title='Selection', message=msg)    # pop up msg for selected value

        if graph_menu.get() == "Total Cases":       # plotting for total cases
            df = pd.read_csv("covid 19 india.csv")  # reading the csv file
            figure(figsize=(8, 8), dpi=80)          # figure size
            x = df['State/UTs']                     # x axis plotting
            y = df['Total Cases']                   # y axis plotting
            plt.title("Total number of cases per state", color='blue', fontsize='17')
            plt.xlabel("States and UT's", fontweight='bold', color='red', fontsize='17')
            plt.xticks(rotation=90)
            plt.ylabel("Total Cases (in Lakhs)", fontweight='bold', color='red', fontsize='17')
            plt.ylim(0, 7000000)                    # y axis limits
            plt.yticks(rotation=90)
            plt.bar(x, y)
            value = askquestion(title="Save this?", message="Do you want to save this figure?")     # whehther to save graph or not
            if value == "yes":
                plt.savefig(f"{graph_menu.get()}.png")   # saving figure/ graph
            else:
                pass
            plt.show()

            def sirValue():
                sir_graph()     # SIR model plotting

            # ----- SIR MODEL -------
            canvas1.create_text(210, 250, text="Want to do SIR model analysis: ", fill="white",
                                font=("Courier", 15, "bold"))
            sir_btn = Button(root, text="Yes!", bg="coral1", command=sirValue)
            canvas1.create_window(400, 250, window=sir_btn)

        elif graph_menu.get() == "Total Deaths":    # plotting for total deaths
            df = pd.read_csv("covid 19 india.csv")
            figure(figsize=(10, 8), dpi=80)
            x = df['State/UTs']
            y = df['Deaths']
            plt.title("Total number of deaths per state", color='blue', fontsize='17')
            plt.xlabel("States", fontweight='bold', color='red', fontsize='17')
            plt.xticks(rotation=90)
            plt.ylabel("Total Deaths (in 20,000)", fontweight='bold', color='red', fontsize='17')
            plt.ylim(0, 150000)
            plt.yticks(rotation=90)
            plt.bar(x, y)
            value = askquestion(title="Save this?", message="Do you want to save this figure?")
            if value == "yes":
                plt.savefig(f"{graph_menu.get()}.png")
            else:
                pass
            plt.show()

            def sirValue():
                sir_graph()
            canvas1.create_text(210, 250, text="Want to do SIR model analysis: ", fill="white",
                                font=("Courier", 15, "bold"))
            sir_btn = Button(root, text="Yes!", bg="coral1", command=sirValue)
            canvas1.create_window(400, 250, window=sir_btn)

        elif graph_menu.get() == "Active Cases":    # plotting for active cases
            df = pd.read_csv("covid 19 india.csv")
            figure(figsize=(10, 8), dpi=80)
            x = df['State/UTs']
            y = df['Active']
            plt.title("Total Number of Active Cases", color='blue', fontsize='17')
            plt.xlabel("States", fontweight='bold', color='red', fontsize='17')
            plt.xticks(rotation=90)
            plt.ylabel("Total Active Cases", fontweight='bold', color='red', fontsize='17')
            plt.ylim(0, 180000)
            plt.yticks(rotation=90)
            plt.bar(x, y)
            value = askquestion(title="Save this?", message="Do you want to save this figure?")
            if value == "yes":
                plt.savefig(f"{graph_menu.get()}.png")
            else:
                pass
            plt.show()

            def sirValue():
                sir_graph()
            canvas1.create_text(210, 250, text="Want to do SIR model analysis: ", fill="white",
                                font=("Courier", 15, "bold"))
            sir_btn = Button(root, text="Yes!", bg="coral1", command=sirValue)
            canvas1.create_window(400, 250, window=sir_btn)

        elif graph_menu.get() == "Recovered":       # plotting for recovered cases
            df = pd.read_csv("covid 19 india.csv")
            figure(figsize=(10, 8), dpi=80, facecolor='#dddd')
            x = df['State/UTs']
            y = df['Discharged']
            plt.title("Total Number of Discharge", color='blue', fontsize='17')
            plt.xlabel("States", fontweight='bold', color='red', fontsize='17')
            plt.xticks(rotation=90)
            plt.ylabel("Total Discharge", fontweight='bold', color='red', fontsize='17')
            plt.ylim(0, 6500000)
            plt.yticks(rotation=90)
            plt.bar(x, y)
            value = askquestion(title="Save this?", message="Do you want to save this figure?")
            if value == "yes":
                plt.savefig(f"{graph_menu.get()}.png")
            else:
                pass
            plt.show()

            def sirValue():
                sir_graph()
            canvas1.create_text(210, 250, text="Want to do SIR model analysis: ", fill="white",
                                font=("Courier", 15, "bold"))
            sir_btn = Button(root, text="Yes!", bg="coral1", cursor='hand2', command=sirValue)
            canvas1.create_window(400, 250, window=sir_btn)

        elif graph_menu.get() == 'None':
            def sirValue():
                sir_graph()
            canvas1.create_text(210, 250, text="Want to do SIR model analysis: ", fill="white",
                                font=("Courier", 15, "bold"))
            sir_btn = Button(root, text="Yes!", bg="coral1", cursor="hand2", command=sirValue)
            canvas1.create_window(400, 250, window=sir_btn)

        else:
            quit()

    # verifying the code
    if veri_code == verify.get():       # comparing the random string value and user input value
        variable = StringVar(root)
        variable.set("one")
        options = ["Total Cases", "Total Deaths", "Active Cases", "Recovered", "None"]
        graph_menu = ttk.Combobox(root, values=options)    # if the verification suceeds, then the combobox is visible
        canvas1.create_text(185, 200, text="Select from the following: ", fill="white",
                            font=("Courier", 15, "bold"))   # text/ label
        canvas1.create_window(420, 200, window=graph_menu)
        graph_menu.bind("<<ComboboxSelected>>", select_value)       # calling the function select value

    else:
        showerror(title="Verification Error", message="Wrong verfication code!!!")  # error box for incorrect verification


# ----- INTIALIZING THE TKINTER WINDOW ------
root = Tk()                             # initializing tkinter root widget
root.geometry("600x450")                # size of the geometry
root.resizable(False, False)
root.title("Covid-19 Analysis")

bg = PhotoImage(file="gui bg.png")      # background of the window
canvas1 = Canvas(root, width=400, height=400)       # Creating canvas
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg, anchor="nw")   # adding the bg image in the canvas as background


# ------ EMAIL INPUT ----------
canvas1.create_text(175, 40, text="Please enter your email: ", fill="white", font=("Courier", 15, "bold"))  # text/label
emailvalue = StringVar()                # taking input as string variable

user_email = Entry(root, textvariable=emailvalue, width=40)     # creating entry widget for taking the email input
user_email_canvas = canvas1.create_window(445, 40, window=user_email)   # adding the email entry widget in the canvas

# ------ EMAIL SUBMIT ---------
submit_email = Button(root, text="Submit Email", bg='coral1', cursor="hand2", command=send_email)   # craeting button
#                                                                                                   for email
submit_email_canvas = canvas1.create_window(175, 70, window=submit_email)

# ------ VERIFICATION CODE ------
canvas1.create_text(237, 140, text="Please enter the verification code: ", fill="white", font=("Courier", 15, "bold"))
#                                                                                                       labels/ text
verify = StringVar()                                        # taking the input as string variable
verify_user = Entry(root, textvariable=verify, width=20)    # entry widget for the verification code
user_verification = canvas1.create_window(510, 139, window=verify_user)

# ------- VERIFICATION BUTTON ---------
submit_otp = Button(root, text="Verify", cursor="hand2", width=10, bg='coral1', command=verify_code)
submit_otp_canvas = canvas1.create_window(175, 169, window=submit_otp)
root.mainloop()
