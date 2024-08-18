# Создал БД
import sqlite3
from datetime import datetime

previous_state = []
previous_action = None


def create_db():
   connection = sqlite3.connect('to_do_list.db')
   cursor = connection.cursor()

   query = '''
   CREATE TABLE IF NOT EXISTS tasks (
   id INTEGER PRIMARY KEY,
   title TEXT NOT NULL,
   due_date TEXT,
   status TEXT NOT NULL DEFAULT 'pending'
   )
   '''
   cursor.execute(query)

   connection.commit()
   connection.close()

create_db()


# Функции работы с задачами
def add_task(title, due_date):

   connection = sqlite3.connect('to_do_list.db')
   cursor = connection.cursor()

   query = '''
   INSERT INTO tasks (title, due_date)
   VALUES (?, ?)
   '''
   cursor.execute(query, (title, due_date))

   connection.commit()
   connection.close()

def view_tasks(status=None):
   connection = sqlite3.connect('to_do_list.db')
   cursor = connection.cursor()

   if status:
      cursor.execute('SELECT * FROM tasks WHERE status=?', (status,))
   else:
      cursor.execute('SELECT * FROM tasks')

   tasks = cursor.fetchall()
   connection.close()

   return tasks

def update_task_status(task_id, new_status):
   connection = sqlite3.connect('to_do_list.db')
   cursor = connection.cursor()

   cursor.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
   if not cursor.fetchone():
      print('Task ID does not exist.')
      connection.close()
      return

   query = '''
   UPDATE tasks
   SET status=?
   WHERE id=?
   '''
   cursor.execute(query, (new_status, task_id))

   connection.commit()
   connection.close()

def delete_task(task_ids):
   if not task_ids:
      print('No tasks to delete.')
      return
   connection = sqlite3.connect('to_do_list.db')
   cursor = connection.cursor()

   query = f'''
   DELETE FROM tasks
   WHERE id IN ({','.join(['?']*len(task_ids))})
   '''
   cursor.execute(query, task_ids)

   connection.commit()
   connection.close()

def save_state(action):
   global previous_state, previous_action
   previous_state = view_tasks()
   previous_action = action

def undo_last_action():
   if not previous_state:
      print('Nothing to undo.')
      return
   
   connection = sqlite3.connect('to_do_list.db')
   cursor = connection.cursor()

   cursor.execute('DELETE FROM tasks')  # Удаляем все текущие задачи
   cursor.executemany('INSERT INTO tasks (id, title, due_date, status) VALUES (?, ?, ?, ?)', previous_state)

   connection.commit()
   connection.close()
   print(f'Last action "{previous_action}" undone.')

def is_valid_date(date_str):
   try:
      datetime.strptime(date_str, '%Y-%m-%d')
      return True
   except ValueError:
      return False

# Применение
def main():
   print('To-do list app')

   while True:
      print('\nOptions:')
      print('1. Add task')
      print('2. View tasks')
      print('3. Update task status')
      print('4. Delete task')
      print('5. Exit')

      choiсe = input('Choose an option (or "b" to go back): ')

      if choiсe.lower() == 'b':
         undo_last_action()
         continue

      if choiсe == '1' or choiсe.lower() == 'add task' or choiсe.lower() == 'add':

         title = input('Enter task title: ')
         if title.lower() == 'b':
            continue
         due_date = input('Enter due date (YYYY-MM-DD): ')
         if due_date.lower() == 'b':
            continue

         while not is_valid_date(due_date):
            print('Invalid date. Please enter the date in YYYY-MM-DD format.')
            due_date = input('Enter due date (YYYY-MM-DD): ')
            if due_date.lower() == 'b':
               continue

         add_task(title, due_date)
         print('Task added')
      
      elif choiсe == '2' or choiсe.lower() == 'view task' or choiсe.lower() == 'view':

         status = input('Filter by status ("p" for pending, "c" for completed or press Enter to skip): ')
         if status.lower() == 'b':
            continue

         if status == 'p' or status == 'pending':
            status = 'pending'
         elif status == 'c' or status == 'completed':
            status = 'completed'
         elif status == '':
            status = ''
         else:
            status = None
         
         status_results = ['pending', 'completed', '']
         while status not in status_results:
            print('Invalid status. Please try again.')
            status = input('Filter by status ("p" for pending, "c" for completed or press Enter to skip): ')

         tasks = view_tasks(status)
         for task in tasks:
            print(task)

      elif choiсe == '3' or choiсe.lower() == 'update task status' or choiсe.lower() == 'update' or choiсe.lower() == 'update task' or choiсe.lower() == 'update status' or choiсe.lower() == 'status':
         task_id = input('Enter task ID to update: ')
         if task_id.lower() == 'b':
            continue
         task_id = int(task_id)

         new_status = input('Enter new status ("p" if pending, "c" if completed): ')
         if new_status.lower() == 'b':
            continue

         if new_status == 'p' or new_status == 'pending':
            new_status = 'pending'
         elif new_status == 'c' or new_status == 'completed':
            new_status = 'completed'
         elif new_status == '':
            print('Status must be pending "p" or completed "c"')
            continue
         else:
            print('Status must be pending "p" or completed "c"')
            continue
            
         update_task_status(task_id, new_status)
         print('Done')

      elif choiсe == '4' or choiсe.lower() == 'delete' or choiсe.lower() == 'delete task':
         task_ids = input('Enter task ID to delete (comma-separated): ')
         if task_ids.lower() == 'b':
            continue
         
         task_ids = [int(id.strip()) for id in task_ids.split(',')]
         delete_task(task_ids)
         print('Task(s) deleted')

      elif choiсe == '5' or choiсe.lower() == 'exit':
         break

      else:
         print('Invalid choise. Please try again.')

if __name__ == '__main__':
   main()
