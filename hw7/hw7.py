import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import pandas as pd
from xmlrpc.client import MAXINT

# ===== Подключение к базе =====
conn = psycopg2.connect(
    host="localhost",
    database="postgres",  # имя вашей базы
    user="postgres",
    password="postgres",
    port=5432
)
cur = conn.cursor()

# ===== Главное окно =====
root = tk.Tk()
root.title("CRUD с PostgreSQL")
root.geometry("500x400")

# ===== Поля ввода =====
ttk.Label(root, text="Имя:").pack(pady=5)
name_entry = ttk.Entry(root)
name_entry.pack(fill="x", padx=10)

ttk.Label(root, text="Возраст:").pack(pady=5)
age_entry = ttk.Entry(root)
age_entry.pack(fill="x", padx=10)

# ===== Поля фильтра по возрасту =====
ttk.Label(root, text="Фильтр по возрасту От:").pack(pady=5)
age_from_entry = ttk.Entry(root)
age_from_entry.pack(fill="x", padx=10)

ttk.Label(root, text="Фильтр по возрасту До:").pack(pady=5)
age_to_entry = ttk.Entry(root)
age_to_entry.pack(fill="x", padx=5)

# ===== Функции =====
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)

def refresh_table():
    """Обновляем таблицу, загружая данные из базы"""
    cur.execute("SELECT * FROM users ORDER BY id")
    for row in table.get_children():
        table.delete(row)
    for row in cur.fetchall():
        table.insert("", "end", values=row)

def add_data():
    name = name_entry.get()
    age = age_entry.get()
    if name == "" or age == "":
        messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
        return
    cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    refresh_table()
    clear_fields()

def update_data():
    selected = table.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите строку для обновления")
        return
    row_id = table.item(selected, "values")[0]
    name = name_entry.get()
    age = age_entry.get()
    if not name or not age:
        messagebox.showwarning("Ошибка", "Поля должны быть заполнены новыми значениями")
        return
    cur.execute("UPDATE users SET name=%s, age=%s WHERE id=%s", (name, age, row_id))
    conn.commit()
    refresh_table()
    clear_fields()

def delete_data():
    selected = table.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите строку для удаления")
        return
    row_id = table.item(selected, "values")[0]
    cur.execute("DELETE FROM users WHERE id=%s", (row_id,))
    conn.commit()
    refresh_table()
    clear_fields()

def export_to_excel():
    """Выгрузка данных в Excel"""
    cur.execute("SELECT * FROM users ORDER BY id")
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Имя", "Возраст"])
    df.to_excel("users.xlsx", index=False)
    messagebox.showinfo("Успех", "Данные успешно экспортированы в users.xlsx")

def top_5_oldest_users():
    """Обновляем таблицу, загружая ТОП-5 самых \"пожилых\" пользователей"""
    cur.execute("SELECT * FROM users ORDER BY age DESC LIMIT 5")
    for row in table.get_children():
        table.delete(row)
    for row in cur.fetchall():
        table.insert("", "end", values=row)

def filter_by_age():
    """Обновляем таблицу, загружая согласно фильтру по возрасту"""
    age_from = age_from_entry.get()
    age_to = age_to_entry.get()
    if not age_from:
        age_from = 0
    if not age_to:
        age_to = MAXINT
    cur.execute("SELECT * FROM users WHERE age BETWEEN %s AND %s", (age_from, age_to))
    for row in table.get_children():
        table.delete(row)
    for row in cur.fetchall():
        table.insert("", "end", values=row)

def statistics():
    """Статистика"""
    cur.execute("SELECT COUNT(*) AS users_number, AVG(age) AS avg_age, MIN(age) AS youngest, MAX(age) AS oldest FROM users")
    result = cur.fetchone()
    messagebox.showwarning("Статистика", f"""
    - Количество пользователей: {result[0]}
    - Средний возраст: {round(result[1])}
    - Самый младший: {result[2]}
    - Самый старший: {result[3]}
    """)

# ===== Кнопки =====
tk.Button(root, text="Добавить", command=add_data, bg="lightgreen", fg="black").pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Удалить", command=delete_data, bg="lightcoral", fg="black").pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Обновить", command=update_data, bg="lightblue", fg="black").pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Очистить поля", command=clear_fields).pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Экспорт в Excel", command=export_to_excel).pack(fill="x", padx=10, pady=5)
tk.Button(root, text="ТОП-5 самых \"пожилых\" пользователей", command=top_5_oldest_users).pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Фильтровать по возрасту", command=filter_by_age).pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Статистика", command=statistics).pack(fill="x", padx=10, pady=5)

# ===== Таблица =====
table = ttk.Treeview(root, columns=("id", "name", "age"), show="headings")
table.heading("id", text="ID")
table.heading("name", text="Имя")
table.heading("age", text="Возраст")
table.pack(fill="both", expand=True, padx=10, pady=10)

# ===== Загрузка данных при старте =====
refresh_table()

# ===== Запуск окна =====
root.mainloop()