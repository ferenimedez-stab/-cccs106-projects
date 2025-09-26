# app_logic.py
import flet as ft
from database import update_contact_db, delete_contact_db, add_contact_db, get_all_contacts_db

def validate_contact_fields(field, field_name, field_val, page):
    """Validates the contact fields."""

    if field_name == "name":
        name_val = field_val.strip()

        if not name_val:
            field.error_text = "Name cannot be empty!"
        elif not name_val.replace(" ", "").replace("-", "").replace("'", "").isalpha():
            field.error_text = "Name can only contain letters!"
        else:
            field.error_text = None

    elif field_name == "phone":
        num_val = field_val.strip()

        if num_val.startswith("0"):
            num_val = num_val[1:]

        if num_val != field_val.strip():
            field.value = num_val

        if not num_val:
            field.error_text = "Phone number cannot be empty!"
        elif not num_val.startswith("9"):
            field.error_text = "Phone number must start with 9!"
        elif len(num_val) != 10:
            field.error_text = "Phone number must be 10 digits!"
        else:
            field.error_text = None

    elif field_name == "email":
        email_val = field_val.strip()

        if not email_val:
            field.error_text = "Email cannot be empty!"
        elif ("@" not in email_val or "." not in email_val.split("@")[-1] or email_val.split("@")[-1].startswith(".") or email_val.endswith(".")):
            field.error_text = "Please enter a valid email address!"
        else:
            field.error_text = None

    else:
        print("Invalid field name.")

    page.update()

def display_contacts(page, contacts_list_view, db_conn, search_query=""):
    '''Fetches and displays contacts from database.'''
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn, search_query)

    contacts = sorted(contacts, key = lambda x: x[1].lower())
    current_let = ""

    for contact in contacts:
        contact_id, name, phone, email = contact
        first_let = name[0].upper() if name else "#"

        initials = "".join([n[0].upper() for n in name.split()[:2]])

        if page.width <= 360:
            font_size_name = 14
            font_size_sub = 12
            avatar_radius = 18
            icon_size = 16
        elif page.width <= 600:
            font_size_name = 16
            font_size_sub = 14
            avatar_radius = 20
            icon_size = 18
        else:
            font_size_name = 18
            font_size_sub = 15
            avatar_radius = 22
            icon_size = 20

        if first_let != current_let:
            if current_let != "":
                contacts_list_view.controls.append(ft.Divider(thickness = 1,
                                                              color = ft.Colors.BLUE_900))

            contacts_list_view.controls.append(ft.Text(first_let,
                                                        size = 20,
                                                        weight = ft.FontWeight.BOLD,
                                                        color = ft.Colors.BLACK))

            current_let = first_let

        contact_card = ft.Card(
            content = ft.Container(
                content = ft.Column([ft.Row([
                                        ft.Column([ft.CircleAvatar(content = ft.Text(initials,
                                                                                     color = ft.Colors.WHITE,
                                                                                     weight = ft.FontWeight.BOLD),
                                                                    bgcolor = ft.Colors.BLUE_400,
                                                                    radius = avatar_radius),

                                                    ft.Icon(ft.Icons.EMAIL,
                                                            size = icon_size - 2,
                                                            color = ft.Colors.BLUE_300)],

                                                    spacing = 15,
                                                    alignment = ft.MainAxisAlignment.CENTER,
                                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER),

                                        ft.Column([ft.Column([ft.Text(name,
                                                                      size = font_size_name,
                                                                      weight = ft.FontWeight.BOLD,
                                                                      text_align = ft.TextAlign.START,
                                                                      color = ft.Colors.BLACK),

                                                              ft.Text(f'+63 {phone[0:3]} {phone[3:6]} {phone[6:]}',
                                                                      color = ft.Colors.BLACK,
                                                                      text_align = ft.TextAlign.START,
                                                                      size = font_size_sub)],
                                                            spacing = 1),

                                                    ft.Text(email,
                                                            color = ft.Colors.BLACK,
                                                            text_align = ft.TextAlign.START,
                                                            size = font_size_sub)],

                                                    spacing = 8,
                                                    alignment = ft.MainAxisAlignment.CENTER,
                                                    expand = True),

                                        ft.Row([ft.IconButton(icon = ft.Icons.CALL,
                                                              icon_color = ft.Colors.BLUE_400,
                                                              icon_size = icon_size,
                                                              tooltip = "Call",
                                                              on_click = lambda _, p = phone: print(f"Calling +63 {p[0:3]} {p[3:6]} {p[6:]}...")),

                                                ft.PopupMenuButton(icon = ft.Icons.MORE_VERT,
                                                                   icon_size = icon_size,
                                                                   icon_color = ft.Colors.BLUE_900,
                                                                   items = [ft.PopupMenuItem(
                                                                            content = ft.Row([ft.Icon(ft.Icons.EDIT,
                                                                                                      size = 17),
                                                                                                    ft.Text("Edit",
                                                                                                            size = 14,
                                                                                                            text_align = ft.TextAlign.CENTER)],
                                                                                                    spacing = 15),
                                                                            height = 12,
                                                                            on_click = lambda _, c = contact: open_edit_dialog(page,
                                                                                                                            c,
                                                                                                                            db_conn,
                                                                                                                            contacts_list_view)),
                                                                        ft.PopupMenuItem(),
                                                                        ft.PopupMenuItem(
                                                                            content = ft.Row([ft.Icon(ft.Icons.DELETE,
                                                                                                      size = 17),
                                                                                                    ft.Text("Delete",
                                                                                                            size = 14,
                                                                                                            text_align = ft.TextAlign.CENTER)],
                                                                                                    spacing = 15),
                                                                            height = 12,
                                                                            on_click=lambda _, cid = contact_id: confirm_delete_dialog(page,
                                                                                                                                cid,
                                                                                                                                name,
                                                                                                                                db_conn,
                                                                                                                                contacts_list_view))])],
                                                spacing = 0,
                                                alignment = ft.MainAxisAlignment.CENTER
                                                    )],

                                            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                                            vertical_alignment = ft.CrossAxisAlignment.CENTER)]),

                                padding = ft.Padding(15, 15, 0, 15),
                                bgcolor = ft.Colors.LIGHT_BLUE_50,
                                border_radius = 10))

        contacts_list_view.controls.append(contact_card)

    page.update()

def add_contact(page, inputs, contacts_list_view, db_conn):
    """Adds a new contact and refreshes the list."""

    name_input, phone_input, email_input = inputs

    add_contact_db(db_conn, name_input.value, phone_input.value, email_input.value)

    for field in inputs:
        field.value = ""

    display_contacts(page, contacts_list_view.content, db_conn)
    page.update()

def delete_contact(page, contact_id, db_conn, contacts_list_view):
    """Deletes a contact and refreshes the list."""

    delete_contact_db(db_conn, contact_id)
    display_contacts(page, contacts_list_view.content, db_conn)

def open_edit_dialog(page, contact, db_conn, contacts_list_view):
    """Opens a dialog to edit a contact's details."""
    contact_id, name, phone, email = contact

    edit_name = ft.TextField(label = "Name",
                             value = name,
                              width = 350,
                              hint_text = "Juan Doe",
                              hint_style = ft.TextStyle(color = ft.Colors.GREY,
                                                       size = 16),
                              autofill_hints = ft.AutofillHint.NAME,
                              )

    edit_phone = ft.TextField(label = "Phone",
                               value = phone,
                               width = 350,
                               prefix_text = "+63 ",
                               prefix_style = ft.TextStyle(size= 16),
                               hint_text = "9XXXXXXXXX",
                               hint_style = ft.TextStyle(color= ft.Colors.GREY,
                                                        size= 16),
                               autofill_hints = ft.AutofillHint.TELEPHONE_NUMBER,
                               input_filter = ft.InputFilter(allow = True,
                                                           regex_string = r"^\d{0,10}$"),
                               keyboard_type = ft.KeyboardType.NUMBER,
                               )

    edit_email = ft.TextField(label = "Email",
                              value = email,
                               width = 350,
                               hint_text = "abc123@domain.com",
                               hint_style = ft.TextStyle(color = ft.Colors.GREY,
                                                        size = 16),
                               autofill_hints = ft.AutofillHint.EMAIL,
                               input_filter = ft.InputFilter(allow = True,
                                                           regex_string = r"^[a-zA-Z0-9@._-]*$"),
                               border_color = ft.Colors.BLACK if page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.WHITE,
                               )

    for field, key in [(edit_name, "name"), (edit_phone, "phone"), (edit_email, "email")]:
        field.on_change = lambda e, f = field, k = key: validate_contact_fields(f, k, f.value, page)
        field.on_blur = lambda e, f = field, k = key: validate_contact_fields(f, k, f.value, page)

    dialog = ft.AlertDialog(modal = True,
                        title = ft.Text("Update Contact Details", size = 20, weight = ft.FontWeight.BOLD),
                        content = ft.Column([edit_name,
                                             edit_phone,
                                             edit_email]),
                        actions = [ft.TextButton("Save", on_click = lambda e: save_and_close(e)),
                                   ft.TextButton("Cancel", on_click = lambda e: setattr(dialog, "open", False) or page.update())])

    success_dialog = ft.AlertDialog(icon = ft.Icon(ft.Icons.CHECK_CIRCLE,
                                                color = ft.Colors.GREEN),
                                title = ft.Text("Contact Updated",
                                                text_align = ft.TextAlign.CENTER),
                                content = ft.Text(spans = [
                                                        ft.TextSpan(f"Contact "),
                                                        ft.TextSpan(name.upper(),style = ft.TextStyle(weight = ft.FontWeight.BOLD, size = 16)),
                                                        ft.TextSpan(' successfully updated!')],
                                                    text_align = ft.TextAlign.CENTER),
                                actions = [ft.TextButton("OK",
                                                            on_click = lambda e: page.close(success_dialog)
                                                            )
                                            ]
                                )

    field_error_dialog = ft.AlertDialog(icon = ft.Icon(ft.Icons.ERROR_OUTLINED,
                                                color = ft.Colors.RED),
                                    title = ft.Text("Error Updating Contact",
                                                    text_align = ft.TextAlign.CENTER),
                                    content = ft.Text("Please check input fields for errors.",
                                                        text_align= ft.TextAlign.CENTER),
                                    actions = [ft.TextButton("OK",
                                                            on_click = lambda e: page.open(dialog) or page.update()
                                                            )
                                                ]
                                            )
    input_required_dialog = ft.AlertDialog(icon = ft.Icon(ft.Icons.ERROR_ROUNDED,
                                                        color = ft.Colors.RED),
                                        title = ft.Text("Error Updating Contact",
                                                        text_align = ft.TextAlign.CENTER, ),
                                        content = ft.Text("All fields are required.",
                                                        text_align= ft.TextAlign.CENTER),
                                        actions = [ft.TextButton("OK",
                                                                on_click = lambda e: page.open(dialog) or page.update()
                                                                )
                                                    ]
                                        )

    system_error_dialog = ft.AlertDialog(icon = ft.Icon(ft.Icons.ERROR_SHARP,
                                                    color = ft.Colors.RED),
                                        title = ft.Text("Error Updating Contact"),
                                        content = ft.Text("An unexpected error occured. Please try agaain later.",
                                                        text_align = ft.TextAlign.CENTER),
                                        actions = [ft.TextButton('OK',
                                                                on_click = lambda e: page.close(system_error_dialog) or page.update()
                                                                )
                                                ]
                                    )
    def save_and_close(e):

        if edit_name.error_text or edit_phone.error_text or edit_email.error_text:
            page.open(field_error_dialog)
            page.update()
            return

        if not (edit_name.value and edit_phone.value and edit_email.value):
            page.open(input_required_dialog)
            page.update()
            return

        try:
            update_contact_db(db_conn, contact_id, edit_name.value, edit_phone.value, edit_email.value)

            page.close(dialog)
            page.update()

            page.open(success_dialog)
            page.update()

            display_contacts(page, contacts_list_view.content, db_conn)

        except Exception:
            page.close(dialog)
            page.open(system_error_dialog)
            page.update()
            return

    dialog.open = True
    page.overlay.append(dialog)
    page.update()

def confirm_delete_dialog(page, contact_id, name, db_conn, contacts_list_view):
    """Opens a confirmation dialog before deleting a contact."""

    def confirm_delete(e):
        page.update()

        delete_contact(page, contact_id, db_conn, contacts_list_view)

        deleted_successfully_dialog = ft.AlertDialog(modal = True,
                                                icon = ft.Icon(ft.Icons.CHECK_CIRCLE,
                                                            color = ft.Colors.GREEN),
                                            title = ft.Text("Contact Deleted", text_align = ft.TextAlign.CENTER),
                                            content = ft.Text(spans = [
                                                            ft.TextSpan(f"Contact "),
                                                            ft.TextSpan(name.upper(), style = ft.TextStyle(weight = ft.FontWeight.BOLD, size = 16)),
                                                            ft.TextSpan(' successfully deleted!')],
                                                        text_align = ft.TextAlign.CENTER),
                                            actions = [ft.TextButton("OK", on_click = lambda e: page.close(deleted_successfully_dialog) or page.update())]
                                            )

        page.open(deleted_successfully_dialog)
        page.update()

    confirm_dialog = ft.AlertDialog(modal = True,
                                    icon = ft.Icon(ft.Icons.WARNING_AMBER,
                                                    color = ft.Colors.ORANGE),
                                    title = ft.Text("Confirm Deletetion", text_align = ft.TextAlign.CENTER),
                                    content = ft.Text("Are you sure you want to delete this contact?"),
                                    actions = [ft.TextButton("Yes", on_click = confirm_delete),
                                               ft.TextButton("No", on_click = lambda e: page.close(confirm_dialog) or page.update())]
    )

    page.open(confirm_dialog)
    page.update()