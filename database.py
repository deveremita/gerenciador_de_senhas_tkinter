# database.py
import sqlite3

class Database:
    def __init__(self, db_path="./db_acessos.db"):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def validate_master_password(self, entered_password):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT senha FROM senha_mestra WHERE id = 1")
            correct_password = cursor.fetchone()

            if correct_password and entered_password == correct_password[0]:
                return True
            else:
                return False

    def get_activities_and_passwords(self):
         with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT id, nome FROM atividades")
            activities = cursor.fetchall()

            result = {}

            for activity in activities:
                activity_id, activity_name = activity
                cursor.execute("SELECT id, nome, email, senha, outros_acessos FROM senhas_atividades WHERE atividade_id = ?", (activity_id,))
                passwords = cursor.fetchall()
                result[activity_name] = {'id': activity_id, 'senhas': passwords}

            return result