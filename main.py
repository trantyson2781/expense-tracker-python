import os
import csv
def load_expense():
    if os.path.exists('expenses.csv'):
        with open('expenses.csv','r') as file:
            reader = csv.DictReader(file)
            expenses = list(reader)
            return expenses
    else:
        return []

def save_expense(expenses):
    fieldnames = ['amount', 'category', 'date']

    with open('expenses.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for expense in expenses:
            writer.writerow(expense)

def add_expense(expenses, amount, category, date):
    expense_dict = {'amount':amount, 'category':category, 'date':date}
    expenses.append(expense_dict)

def show_summary(expenses):
    summary_string = []
    months = set(expense['date'][:7] for expense in expenses)
    for month in sorted(months): 
        total_monthly_expense = sum(float(exp['amount']) for exp in expenses if exp['date'].startswith(month))
        summary_string.append(f'{month}: ${total_monthly_expense:.2f}')
    categories = set(expense['category'] for expense in expenses)
    for category in sorted(categories):
        total_expense_by_category = sum(float(exp['amount']) for exp in expenses if exp['category'] == category)
        summary_string.append(f'{category}: ${total_expense_by_category:.2f}')  
    return '\n'.join(summary_string)

def get_expense_text(expenses):
    lines = []
    for i,exp in enumerate(expenses):
        line = f"{i+1}: Amount: {exp['amount']} | Category: {exp['category']} | Date: {exp['date']}"
        lines.append(line)
    return '\n'.join(lines)


def delete():
    pass

import tkinter as tk
from tkinter import messagebox
def main():
    expenses = load_expense()

    root = tk.Tk()
    root.title("Expense Tracker")
    root.geometry("300x300")

    tk.Button(root, text="Add Expense", width=20, command=lambda: open_add_expense(expenses)).pack(pady=10)
    tk.Button(root, text="View Summary", width=20, command=lambda: show_summary_popup(expenses)).pack(pady=10)
    tk.Button(root, text="View All Expenses", width=20, command=lambda: view_all_expenses(expenses)).pack(pady=10)
    tk.Button(root, text="Edit", width=20, command=lambda: edit_entry(expenses)).pack(pady=10)
    tk.Button(root, text ="Delete Entry", width=20, command=lambda: delete_entry(expenses)).pack(pady=10)
    tk.Button(root, text="Save and Exit", width=20, command=lambda: save_and_exit(root, expenses)).pack(pady=10)


    root.mainloop()


def open_add_expense(expenses):
    window = tk.Toplevel()
    window.geometry("300x200")
    tk.Label(window, text ='Amount').pack()
    amount_entry = tk.Entry(window)
    amount_entry.pack()

    tk.Label(window, text ='Category').pack()
    category_entry = tk.Entry(window)
    category_entry.pack()

    tk.Label(window, text ='Date(YYYY-MM-DD)').pack()
    date_entry = tk.Entry(window)
    date_entry.pack()

    def handle_submit():
        amount = amount_entry.get()
        category = category_entry.get()
        date = date_entry.get()

        if not amount or not category or not date:
            messagebox.showerror('Missing Data','Please fill out all fields')
            return
        
        add_expense(expenses, amount, category, date)
        messagebox.showinfo('Success!','Expense Added')
        window.destroy()
    tk.Button(window,text = 'Add expense',command=handle_submit).pack()


 
def show_summary_popup(expenses):
    window = tk.Toplevel()
    window.title("Expense Summary")
    window.geometry("300x400")

    summary_box = tk.Text(window)
    summary_string = show_summary(expenses)
    summary_box.insert('1.0', summary_string)
    summary_box.pack()
    close_button = tk.Button(window, text= 'Close', command= window.destroy)
    close_button.pack(pady = 10)

def view_all_expenses(expenses):
    window = tk.Toplevel()
    window.title("All Expenses")
    window.geometry("500x500")
    text_box = tk.Text(window, wrap="word")
    scrollbar = tk.Scrollbar(window, command=text_box.yview)
    text_box.configure(yscrollcommand=scrollbar.set)

    all_expenses = get_expense_text(expenses)
    text_box.insert("1.0", all_expenses)
    text_box.config(state='disabled')
    text_box.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")




def save_and_exit(root,expenses):
    save_expense(expenses) 
    root.destroy()
    tk.Button(root, text="Save and Exit", width=20, command=lambda: save_and_exit(root, expenses)).pack(pady=10)
          
def edit_entry(expenses):
    window = tk.Toplevel()
    window.title("Edit Expenses")
    window.geometry("400x400")

    tk.Label (window,text = 'Enter expense index: ').pack()
    edit_index = tk.Entry(window)
    edit_index.pack()

    amount_entry = tk.Entry(window)
    category_entry = tk.Entry(window)
    date_entry = tk.Entry(window)

    def load_row():
        index_str = edit_index.get()
        selected_expense = expenses[int(index_str)-1]
        amount_entry.delete(0,tk.END)
        amount_entry.insert(0,selected_expense['amount'])
        category_entry.delete(0, tk.END)
        category_entry.insert(0, selected_expense['category'])
        date_entry.delete(0, tk.END)
        date_entry.insert(0, selected_expense['date'])
    tk.Button(window, text = "Load", width = 20, command= lambda: load_row()).pack(pady=10)
    amount_entry.pack()
    category_entry.pack()
    date_entry.pack()


    def save_edits():
        index = int(edit_index.get())-1
        new_amount = amount_entry.get()
        new_category = category_entry.get()
        new_date = date_entry.get()
        if new_amount:
            expenses[index]['amount'] = new_amount
        if new_category:
            expenses[index]['category'] = new_category
        if new_date:
            expenses[index]['date'] = new_date
        save_expense(expenses)     
        messagebox.showinfo("Updated","Expense updated successfully")   
    tk.Button(window, text="Save Changes", width=20, command=save_edits).pack(pady=10)

   
def delete_entry(expenses):
    window = tk.Toplevel()
    window.title("Delete Expenses")
    window.geometry('200x200')

    tk.Label (window,text = 'Enter expense index: ').pack()
    delete_index = tk.Entry(window)
    delete_index.pack()
   
    def handle_delete():
        index= delete_index.get()   
        expenses.pop(int(index)-1)
        messagebox.showinfo('Delete','Deleted successfully')
        window.destroy()

    tk.Button(window,text='Delete',command=handle_delete).pack()
    
if __name__ == '__main__':
    main()

