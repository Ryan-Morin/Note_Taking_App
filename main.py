import tkinter as tk
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize Firebase app
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)

# Create a Firestore client
db = firestore.client()

# Geometry variable for the main window
geometry = "400x400"

# Model
class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def save(self):
        # Save the note to Firebase
        doc_ref = db.collection("notes").document()
        doc_ref.set({"title": self.title, "content": self.content})

    @staticmethod
    def get_all_notes():
        # Get all notes from Firebase
        notes = []
        docs = db.collection("notes").stream()
        for doc in docs:
            notes.append(Note(doc.to_dict()["title"], doc.to_dict()["content"]))
        return notes

# View
class NoteView(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Note Taking App")

        # Create text widgets for title and content
        self.title_text = tk.StringVar()
        title_entry = tk.Entry(self, textvariable=self.title_text)
        title_entry.pack()

        self.content_text = tk.StringVar()
        content_entry = tk.Entry(self, textvariable=self.content_text)
        content_entry.pack()

        # Create a save button
        save_button = tk.Button(self, text="Save", command=self.save_note)
        save_button.pack()

class NoteListView(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Note List")

        # Get all notes
        notes = Note.get_all_notes()

        # Create a listbox to display notes
        self.listbox = tk.Listbox(self)
        for note in notes:
            self.listbox.insert(tk.END, note.title)
        self.listbox.pack()

        # Create a back button
        back_button = tk.Button(self, text="Back", command=self.back)
        back_button.pack()

    def back(self):
        self.destroy()

# Controller
class NoteController:
    def __init__(self, parent):
        self.view = NoteView(parent)

class NoteListController:
    def __init__(self, parent):
        self.view = NoteListView(parent)

# Create the main window
root = tk.Tk()
root.title("Note Taking App")


# Create a new note button
new_note_button = tk.Button(root, text="New Note", command=lambda: NoteController(root))
new_note_button.pack()

# Create a view notes button
view_notes_button = tk.Button(root, text="View Notes", command=lambda: NoteListController(root))
view_notes_button.pack()

root.mainloop()

