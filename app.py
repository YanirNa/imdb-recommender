import tkinter as tk
from tkinter import *
from tkinter import messagebox
import pandas as pd
from function import *


class MovieRecommendationUI:
    def __init__(self, master):
        self.master = master

        master.title("Movie Recommendation System")
        self.title_var = tk.StringVar()
        self.genre_var = tk.StringVar()
        self.director_var = tk.StringVar()
        self.duration_var = tk.StringVar()

        # Labels
        self.label_title = Label(master, text="Enter Movie Title:")
        self.label_genres = Label(master, text="Enter Preferred Genre:")
        self.label_director = Label(master, text="Enter Preferred Director:")
        self.label_duration = Label(master, text="Enter Duration Range (start, end):")

        # Entry Widgets
        self.entry_title = Entry(master,textvariable = self.title_var, font=('calibre',10,'normal'))
        self.entry_genres = Entry(master,textvariable = self.genre_var, font=('calibre',10,'normal'))
        self.entry_director = Entry(master,textvariable = self.director_var, font=('calibre',10,'normal'))
        self.entry_duration = Entry(master,textvariable = self.duration_var, font=('calibre',10,'normal'))

        # Text Display
        self.text_display = Text(master, height=10, width=50)
  

        # Button
        self.button_title = Button(master, text="Get Recommendations by Other Movie", command=self.display_recommendations)
        self.button_genre= Button(master, text="Get Recommendations by Genre", command=self.display_recommendations)
        self.button_director= Button(master, text="Get Recommendations by Director", command=self.display_recommendations)
        self.button_duration= Button(master, text="Get Recommendations by Duration", command=self.display_recommendations)

        # Layout
        self.label_title.grid(row=0, column=0, sticky="w")
        self.entry_title.grid(row=0, column=1, sticky="ew")
        self.button_title.grid(row=0, column=2, sticky="e")

        self.label_genres.grid(row=1, column=0, sticky="w")
        self.entry_genres.grid(row=1, column=1, sticky="ew")
        self.button_genre.grid(row=1, column=2, sticky="e")

        self.label_director.grid(row=2, column=0, sticky="w")
        self.entry_director.grid(row=2, column=1, sticky="ew")
        self.button_director.grid(row=2, column=2, sticky="e")

        self.label_duration.grid(row=3, column=0, sticky="w")
        self.entry_duration.grid(row=3, column=1, sticky="ew")
        self.button_duration.grid(row=3, column=2, sticky="e")

    def display_recommendations(self):
        # Get the text of the button that was clicked
        button_text = self.master.focus_get().cget("text")
        
        #recommend to initilize
        result_df = pd.DataFrame()

        # check which button was clicked and call the corresponding recommendation function
        # user enter str-> str saved as a var-> check which button pressed -> send the str to the right funcrion
        if button_text == "Get Recommendations by Other Movie":
            title = self.entry_title.get()
            result_df = get_reccommendation_other_movies(title)
        
        elif button_text == "Get Recommendations by Genre":
            genre = self.entry_genres.get()
            result_df = recommend_by_genre(genre)

        elif button_text == "Get Recommendations by Director":
            director = self.entry_director.get()
            result_df = recommend_by_director(director)

        elif button_text == "Get Recommendations by Duration":
            duration_range = self.entry_duration.get()
            duration_range= tuple(duration_range)
            result_df = recommend_by_duration(duration_range)

        
        #attempt to show the result on new windows
        recommend_window = Toplevel(self.master)
        recommend_window.title("Recommendations")
        text_display_new = Text(recommend_window, height=10, width=50)
        text_display_new.pack()
        # insert the result_df into the Text widget in the new window
        text_display_new.insert(END, result_df.to_string(index=False))


if __name__ == "__main__":
    root = Tk()
    root.geometry("600x200")
    app = MovieRecommendationUI(root)
    root.mainloop()