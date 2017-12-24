from logic.users import Users


class Actions:
    def initialize_actions(self, socketio):
        users = Users(socketio)
        return {
            "login": {
                "description": "",
                "method": "POST",
                "parameters": ["email", "password"],
                "headers": [],
                "function": users.login
            },
            "register": {
                "description": "",
                "method": "POST",
                "parameters": ["email", "f_name", "l_name", "m_name", "phone", "username", "title"],
                "headers": [],
                "function": users.register
            },
            "account_exists": {
                "description": "Checks if an email exists in the system. On success returns title and last_name",
                "method": "POST",
                "parameters": ["email"],
                "headers": [],
                "function": users.user_exists
            }
        }
