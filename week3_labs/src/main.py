import flet as ft
import mysql.connector
from db_connection import connect_db

def main(page: ft.Page):
    page.window.center()
    page.window.frameless = True
    page.window.title_bar_buttons_hidden = True
    page.title = "User Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.height = 350
    page.window.width = 400
    page.bgcolor = ft.Colors.AMBER_ACCENT

    title = ft.Text("User Login",
                text_align = ft.TextAlign.CENTER,
                size = 20,
                weight = ft.FontWeight.BOLD,
                font_family = "Arial")

    username = ft.TextField(label = "User name",
                          hint_text = "Enter your user name",
                          helper_text = "This is your unique identifier",
                          width = 300,
                          autofocus = True,
                          disabled = False,
                          icon = ft.Icons.PERSON,
                          bgcolor = ft.Colors.LIGHT_BLUE_ACCENT)

    password = ft.TextField(label = "Password",
                            hint_text = "Enter your password",
                            helper_text = "This is your secret key",
                            width = 300,
                            disabled = False,
                            password = True,
                            can_reveal_password = True,
                            icon = ft.Icons.PASSWORD,
                            bgcolor = ft.Colors.LIGHT_BLUE_ACCENT)


    def login_click(e):
        success_dialog = ft.AlertDialog(
            icon = ft.Icon(ft.Icons.CHECK_CIRCLE, color = ft.Colors.GREEN),
            title = ft.Text("Login Successful", text_align = ft.TextAlign.CENTER),
            content = ft.Text(f'Welcome, {username.value}!',
                              text_align = ft.TextAlign.CENTER),
            actions = [
                ft.TextButton("OK", on_click = lambda e: page.close(success_dialog))
            ]
        )

        failure_dialog = ft.AlertDialog(
            icon = ft.Icon(ft.Icons.ERROR, color = ft.Colors.RED),
            title = ft.Text("Login Failed", text_align = ft.TextAlign.CENTER),
            content = ft.Text("Invalid username or password",
                              text_align = ft.TextAlign.CENTER),
            actions = [
                ft.TextButton("OK", on_click = lambda e: page.close(failure_dialog))
            ]
        )

        invalid_input_dialog = ft.AlertDialog(
            icon = ft.Icon(ft.Icons.INFO, color = ft.Colors.BLUE),
            title = ft.Text("Input Error", text_align = ft.TextAlign.CENTER),
            content = ft.Text("Please enter username and password",
                              text_align = ft.TextAlign.CENTER),
            actions = [
                ft.TextButton("OK", on_click = lambda e: page.close(invalid_input_dialog))
            ]
        )

        database_error_dialog = ft.AlertDialog(
            title = ft.Text("Database Error"),
            content = ft.Text("An error occurred while connecting to the database"),
            actions = [
                ft.TextButton("OK", on_click = lambda e: page.close(database_error_dialog))
            ]
        )

        if username.value == "" or password.value == "":
            page.open(invalid_input_dialog)
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            query = "SELECT 1 FROM users WHERE username = %s AND password = %s LIMIT 1"
            cursor.execute(query, (username.value, password.value))

            result = cursor.fetchone() is not None

            cursor.close()
            conn.close()

            if result:
                page.open(success_dialog)

            else:
                page.open(failure_dialog)

            page.update()

        except mysql.connector.Error:
            page.open(database_error_dialog)
            page.update()

    login_button = ft.ElevatedButton("Login",
                                     on_click = login_click,
                                     width = 100,
                                     icon = ft.Icons.LOGIN)

    page.add(title)
    page.add(ft.Container(content = ft.Column(controls=[username, password],
                                              spacing = 20)
                        )
    )
    page.add(ft.Container(content = login_button,
                          alignment = ft.alignment.top_right,
                          margin = ft.Margin(0, 20, 40, 0)))

ft.app(target = main)