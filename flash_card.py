import sqlite3
import sys


class flashcards:
    def __init__(self, banco):
        self.conn = sqlite3.connect(banco)
        cursor = self.conn.cursor()
        cursor.execute(
        "CREATE TABLE IF NOT EXISTS Questions(id INTEGER PRIMARY KEY, Content TEXT, Title TEXT, Ask TEXT, Answer TEXT)")
        self.conn.commit()

    def insert_questions(self, Content,  Title, Ask, Answer):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Questions ( Content, Title, Ask, Answer) VALUES(?,?,?,?)", (Content, Title, Ask, Answer))
        self.conn.commit()


    def remove_questions(self, id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Questions WHERE id = ?", (id))
        self.conn.commit()

    def search_questions(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT Ask FROM Questions;")
        questions = cursor.fetchone()
        for question in questions:
            print(f"Question: {questions[0]}")
            return question



class menu:
    #ALWAYS USE self.yourfunction() TO USE YOUR FUNCTION 
    def __init__(self):
        self.system = flashcards("database.db")
    def show_painel(self):

        painel = ["""###############\n\n

    MENU PAINEL USAGE:

    1.Add a flash card;
    2.Remove a flash card;
    3.Search for a flash card.

    ###############\n\nChoose: """]
        result = int(input(painel[0]))
        if result == 1:
            self.add_flashcard()    
        elif result == 2:
            self.remove_flashcard()
        elif result == 3:
            self.search_flashcard()    

    def add_flashcard(self):
        try:
            system = flashcards("database.db")
            content = input("Content: ")
            title = input("\nTitle:")
            print("Ask: (Pressione Ctrl + D quando terminar)")
            ask = sys.stdin.read()
            answer = input("\nAnswer: ")


            system.insert_questions(content, title, ask, answer)

        except KeyboardInterrupt:
            print("\nEntrada de texto interrompida. O programa será encerrado.")
            
        except Exception as e:
            print("Error to add flash cards: ",e)

    def remove_flashcard(self):
        #remove_questions is a string not a interger.
        system = flashcards("database.db")
        system.remove_questions(input("What is the id?: "))        

    def search_flashcard(self):
        try:
            system = flashcards("database.db")
            system.search_questions()
        except Exception as e:
            print("None content was added.")        


menu_run = menu()
menu_run.show_painel()



    
