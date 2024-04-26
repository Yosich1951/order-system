import tkinter as tk
from tkinter import ttk
import sqlite3

# Создаём базу данных. Работаем сверху, после блока импорта.
def init_db():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    order_details TEXT NOT NULL,
    status TEXT NOT NULL)
    """)
    conn.commit()
    conn.close()

# Создаём функцию добавления заказа. Здесь же устанавливаем автоматическое
# назначение статуса ‘Новый’.
def add_order():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, 'Новый')",
                 (customer_name_entry.get(), order_details_entry.get()))
    conn.commit()
    conn.close()
    # очистить поля ввода
    customer_name_entry.delete(0, tk.END)
    order_details_entry.delete(0, tk.END)
    # обновить таблицу
    view_orders()


# Создаём функцию для того, чтобы внесённые данные отображались в таблице
# в открытом окне:
def view_orders():
    for i in tree.get_children():
        tree.delete(i)
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

# создаем окно интерфейса
app = tk.Tk()
app.title('Система управления заказами')
# добавляем надписи
tk.Label(app, text = 'Имя клиента').pack()
# создаем поле для ввода имени клиента
customer_name_entry = tk.Entry(app)
customer_name_entry.pack()
# создаем поля для деталей заказа
tk.Label(app, text = 'Детали заказа').pack()
order_details_entry = tk.Entry(app)
order_details_entry.pack()
# создаем кнопку, которая будет добавлять введенные данные в таблицу
add_button = tk.Button(app, text='Добавить заказ', command = add_order)
add_button.pack()
# используем новую функцию
columns = ("id", "customer_name", "oder_details", "status")
tree = ttk.Treeview(app, columns=columns, show="headings")
# используем цикл для переборки кортежа
for column in columns:
    tree.heading(column, text=column)
tree.pack()
# Дополняем финальную строчку, пишем перед ней:
init_db()
view_orders()

# вводим цикл
app.mainloop()

