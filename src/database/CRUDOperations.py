import sqlite3

# CRUD 操作示例
class CRUDOperations:
    def __init__(self, db_name="app_data.db"):
        self.db_name = db_name

    def insert_user(self, username, email):
        """插入用户数据"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, email) VALUES (?, ?)",
                    (username, email)
                )
                conn.commit()
                print(f"用户 {username} 插入成功，ID: {cursor.lastrowid}")
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"插入用户错误: {e}")
            return None

    def get_all_users(self):
        """获取所有用户"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
                users = cursor.fetchall()
                return users
        except sqlite3.Error as e:
            print(f"获取用户错误: {e}")
            return []

    def update_user_email(self, user_id, new_email):
        """更新用户邮箱"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET email = ? WHERE id = ?",
                    (new_email, user_id)
                )
                conn.commit()
                if cursor.rowcount > 0:
                    print(f"用户 {user_id} 邮箱更新成功")
                    return True
                return False
        except sqlite3.Error as e:
            print(f"更新用户错误: {e}")
            return False

    def delete_user(self, user_id):
        """删除用户"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    print(f"用户 {user_id} 删除成功")
                    return True
                return False
        except sqlite3.Error as e:
            print(f"删除用户错误: {e}")
            return False


# 使用示例
if __name__ == "__main__":
    crud = CRUDOperations()

    # 插入数据
    user_id = crud.insert_user("john_doe", "john@example.com")
    crud.insert_user("jane_smith", "jane@example.com")

    # 查询数据
    users = crud.get_all_users()
    print("所有用户:", users)

    # 更新数据
    crud.update_user_email(user_id, "john.new@example.com")

    # 删除数据
    # crud.delete_user(user_id)