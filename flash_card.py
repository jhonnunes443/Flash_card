import sqlite3
import sys
import random
#import time
import os


class Flashcards:
    def __init__(self, banco):
        self.conn = sqlite3.connect(banco)
        cursor = self.conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Questions(id INTEGER PRIMARY KEY, Content TEXT, Title TEXT, Ask TEXT, Answer TEXT)")
        self.conn.commit()

    def insert_questions(self, Content, Title, Ask, Answer):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Questions (Content, Title, Ask, Answer) VALUES(?,?,?,?)", (Content, Title, Ask, Answer))
        self.conn.commit()

    def remove_questions(self, id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Questions WHERE id = ?", (id,))
        self.conn.commit()

    def search_questions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, Content, Title FROM Questions;")
        for row in cursor.fetchall():
            print(row[0],"|",row[1],"|",row[2])


    def play(self, content_filter=None):
        try:
            os.system('cls' if os.name == 'nt' else 'clear') 
            cursor = self.conn.cursor()
            if content_filter is None:
                options = cursor.execute("SELECT DISTINCT Content FROM Questions")
                options = cursor.fetchall()
                print("Available content options:")
            for index, option in enumerate(options, start=1):
                print(f"{index}. {option[0]}")
            
            choice_number = int(input("Type the number of the Content you choose: "))
            
            if 1 <= choice_number <= len(options):
                content_filter = options[choice_number - 1][0]
            else:
                print("Invalid choice. Please choose a number within the range.")
                return  

            if content_filter:
                cursor.execute("SELECT Ask FROM Questions WHERE Content=? ",(content_filter,))
                questions = cursor.fetchall()
                random.shuffle(questions)

                for question in questions:
                    print("Question:", question[0])
                    print("Type '1' to see the answer or 'q' to quit: ")
                    answer_option = input()

                    if answer_option == "1":
                        cursor.execute("SELECT Answer FROM Questions WHERE Ask=?", (question[0],))
                        answer = cursor.fetchone()
                        print("Answer:", answer[0])
                        input("Pressione Enter para continuar...")
                        os.system('cls' if os.name == 'nt' else 'clear')  
                    elif answer_option.lower() == "q":
                        break
                    else:
                        print("Invalid input. Please type '1' to see the answer or 'q' to quit.")

        except Exception as e:
            print('Error:', e)
        



class Menu:
    def __init__(self):
        self.system = Flashcards("database.db")


    def show_panel(self):
        try:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear') 
                print("##########\nMy Flash Cards:\n")
                self.search_flashcard()
                panel = [
                    """\n###############

MENU PANEL USAGE:

1. Add a flash card;
2. Remove a flash card;
3. Update;
4. Play.
5. Exit

###############

Choose: """
                ]
                try:
                    result = int(input(panel[0]))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if result == 1:
                    self.add_flashcard()
                elif result == 2:
                    self.remove_flashcard()
                elif result == 3:
                    self.search_flashcard()
                elif result == 4:
                    self.play()
                elif result == 5:
                    self.exit()
        except Exception as e:
            print("\nProgram fail",e)
        except KeyboardInterrupt:
            print("\nFinishing the program...")
    

    def add_flashcard(self):
        try:
            system = Flashcards("database.db")
            content = input("Content: ")
            title = input("\nTitle: ")
            print("Ask: (Press Ctrl + D when finished)")
            ask = sys.stdin.read()
            print("Answer: (Press Ctrl + D when finished)")
            answer = sys.stdin.read()

            system.insert_questions(content, title, ask, answer)

        except KeyboardInterrupt:
            print("\nText input interrupted. The program will exit.")

        except Exception as e:
            print("Error adding flash cards:", e)

    def remove_flashcard(self):
        self.system.remove_questions(input("What is the id?: "))

    def search_flashcard(self):
        try:
            self.system.search_questions()
        except None:
            print("No content was added.")

    def play(self):
        try:
            self.system.play()
        except None:
            print("No content was added.")
    def exit(self):
        sys.exit()


menu_run = Menu()
menu_run.show_panel()




    
