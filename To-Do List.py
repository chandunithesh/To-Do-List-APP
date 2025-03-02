import tkinter as tk
from tkinter import messagebox, simpledialog

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List App")
        self.root.geometry("500x700")
        self.root.config(bg="#f4f4f9")  # Soft background color

        # List to store tasks
        self.tasks = []

        # Title of the App
        self.title_label = tk.Label(self.root, text="Todo List", font=("Roboto", 24, "bold"), bg="#f4f4f9", fg="#333")
        self.title_label.pack(pady=20)

        # Task input fields
        self.input_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.input_frame.pack(pady=10)

        self.title_label_input = tk.Label(self.input_frame, text="Task Title", font=("Roboto", 12), bg="#f4f4f9", fg="#333")
        self.title_label_input.grid(row=0, column=0, padx=10, pady=5)

        self.title_entry = tk.Entry(self.input_frame, font=("Roboto", 12), width=30, bd=2, relief="solid")
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        self.desc_label_input = tk.Label(self.input_frame, text="Task Description", font=("Roboto", 12), bg="#f4f4f9", fg="#333")
        self.desc_label_input.grid(row=1, column=0, padx=10, pady=5)

        self.desc_entry = tk.Entry(self.input_frame, font=("Roboto", 12), width=30, bd=2, relief="solid")
        self.desc_entry.grid(row=1, column=1, padx=10, pady=5)

        # Add task button
        self.add_button = tk.Button(self.root, text="Add Task", width=20, height=2, font=("Roboto", 12), bg="#4CAF50", fg="white", command=self.add_task, relief="flat")
        self.add_button.pack(pady=10)

        # Task list display
        self.task_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.task_frame.pack(pady=10)

        # Scrollable canvas for tasks
        self.tasks_canvas = tk.Canvas(self.task_frame, bg="#f4f4f9", height=300)
        self.tasks_canvas.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.scrollbar = tk.Scrollbar(self.task_frame, orient="vertical", command=self.tasks_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tasks_canvas.config(yscrollcommand=self.scrollbar.set)

        # Frame inside canvas to hold tasks
        self.tasks_inner_frame = tk.Frame(self.tasks_canvas, bg="#f4f4f9")
        self.tasks_canvas.create_window((0, 0), window=self.tasks_inner_frame, anchor="nw")

        self.tasks_inner_frame.bind(
            "<Configure>",
            lambda e: self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
        )

        # Edit and Delete buttons
        self.button_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.button_frame.pack(pady=10)

        self.edit_button = tk.Button(self.button_frame, text="Edit Task", width=20, height=2, font=("Roboto", 12), bg="#FF9800", fg="white", command=self.edit_task, relief="flat")
        self.edit_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(self.button_frame, text="Delete Task", width=20, height=2, font=("Roboto", 12), bg="#F44336", fg="white", command=self.delete_task, relief="flat")
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.selected_task_index = None  # Track selected task index for edit/delete

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()

        if not title or not description:
            messagebox.showwarning("Input Error", "Both title and description are required.")
            return

        task = {"title": title, "description": description, "completed": False}
        self.tasks.append(task)
        self.update_task_list()
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

    def edit_task(self):
        if self.selected_task_index is None:
            messagebox.showwarning("Selection Error", "Please select a task to edit.")
            return

        task = self.tasks[self.selected_task_index]
        new_title = simpledialog.askstring("Edit Title", "Enter new task title:", initialvalue=task['title'], parent=self.root)
        if new_title is None:
            return

        new_desc = simpledialog.askstring("Edit Description", "Enter new task description:", initialvalue=task['description'], parent=self.root)
        if new_desc is None:
            return

        task["title"] = new_title
        task["description"] = new_desc
        self.update_task_list()

    def delete_task(self):
        if self.selected_task_index is None:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
            return

        del self.tasks[self.selected_task_index]
        self.selected_task_index = None
        self.update_task_list()

    def toggle_task_completion(self, idx):
        task = self.tasks[idx]
        task["completed"] = not task["completed"]
        self.update_task_list()

    def update_task_list(self):
        for widget in self.tasks_inner_frame.winfo_children():
            widget.destroy()

        for idx, task in enumerate(self.tasks):
            task_frame = tk.Frame(self.tasks_inner_frame, bg="#f4f4f9")
            task_frame.pack(fill=tk.X, pady=5)

            # Checkbox for task completion
            var = tk.IntVar(value=1 if task["completed"] else 0)
            checkbox = tk.Checkbutton(task_frame, text=f"{task['title']} - {task['description']}",
                                      variable=var, font=("Roboto", 12), bg="#f4f4f9", fg="#333", 
                                      command=lambda idx=idx: self.toggle_task_completion(idx))
            checkbox.pack(side=tk.LEFT)

            # Button to select task for edit/delete
            task_select_button = tk.Button(task_frame, text="Select", command=lambda idx=idx: self.select_task(idx))
            task_select_button.pack(side=tk.RIGHT, padx=10)

    def select_task(self, idx):
        self.selected_task_index = idx
        messagebox.showinfo("Task Selected", f"Task '{self.tasks[idx]['title']}' has been selected for editing or deletion.")

# Create main window
root = tk.Tk()
todo_app = TodoApp(root)

# Run the app
root.mainloop()
