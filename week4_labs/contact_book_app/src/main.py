# main.py
import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact, validate_contact_fields

def main(page: ft.Page):

    page.fonts = {
        "Canva Sans": "/CanvaSans-Medium.woff2"
    }

    page.theme = ft.Theme(font_family = "Canva Sans")

    page.title = "Contact Book"

    page.vertical_alignment = ft.MainAxisAlignment.START

    page.window.width = 500

    page.window.height = 700

    page.window.center()

    page.window.bgcolor = ft.Colors.LIGHT_BLUE_50

    db_conn = init_db()

    page.theme_mode = ft.ThemeMode.LIGHT

    # ------------------------- iNPUT FIELDS -------------------------

    name_input = ft.TextField(label = "Name",
                              icon = ft.Icons.PERSON,
                              expand = True,
                              border_radius = 7,
                              border_color = ft.Colors.LIGHT_BLUE_500,
                              hint_text = "Juan Doe",
                              hint_style = ft.TextStyle(color = ft.Colors.GREY,
                                                       size = 15),
                              autofill_hints = ft.AutofillHint.NAME,
                              error_style = ft.TextStyle(size = 10),
                              text_vertical_align = ft.VerticalAlignment.CENTER,
                              content_padding = ft.Padding(10, 0, 10, 0)
                              )

    phone_input = ft.TextField(label = "Phone",
                               icon = ft.Icons.PHONE,
                               expand = True,
                               border_radius = 7,
                               border_color = ft.Colors.LIGHT_BLUE_500,
                               prefix_text = "+63 ",
                               prefix_style = ft.TextStyle(size = 16),
                               hint_text = "9XXXXXXXXX",
                               hint_style = ft.TextStyle(color = ft.Colors.GREY,
                                                        size = 15),
                               autofill_hints = ft.AutofillHint.TELEPHONE_NUMBER,
                               input_filter = ft.InputFilter(allow = True,
                                                           regex_string = r"^\d{0,10}$"),
                               keyboard_type = ft.KeyboardType.NUMBER,
                               error_style = ft.TextStyle(size = 10),
                               text_vertical_align = ft.VerticalAlignment.CENTER,
                               content_padding = ft.Padding(10, 0, 10, 0)
                               )

    email_input = ft.TextField(label = "Email",
                               icon = ft.Icons.EMAIL,
                               expand = True,
                               border_radius = 7,
                               border_color = ft.Colors.LIGHT_BLUE_500,
                               hint_text = "abc123@domain.com",
                               hint_style = ft.TextStyle(color = ft.Colors.GREY,
                                                        size = 16),
                               autofill_hints = ft.AutofillHint.EMAIL,
                               input_filter = ft.InputFilter(allow = True,
                                                           regex_string = r"^[a-zA-Z0-9@._-]*$"),
                               error_style = ft.TextStyle(size = 10),
                               text_vertical_align = ft.VerticalAlignment.CENTER,
                               content_padding = ft.Padding(10, 0, 10, 0)
                               )


    # ------------------------- INPUT VALIDATION -------------------------

    for field, key in [(name_input, "name"), (phone_input, "phone"), (email_input, "email")]:
        field.on_change = lambda e, f = field, k = key: validate_contact_fields(f, k, f.value, page)
        field.on_blur = lambda e, f = field, k = key: validate_contact_fields(f, k, f.value, page)

    def add_contact_click(e):

        success_dialog = ft.AlertDialog(icon = ft.Icon(ft.Icons.CHECK_CIRCLE,
                                                       color = ft.Colors.GREEN),
                                        title = ft.Text("Contact Saved",
                                                        text_align = ft.TextAlign.CENTER),
                                        content = ft.Text(spans = [
                                                                ft.TextSpan(f"Contact "),
                                                                ft.TextSpan(f'{name_input.value.upper() if name_input.value else ""}', style = ft.TextStyle(weight = ft.FontWeight.BOLD, size = 16)),
                                                                ft.TextSpan(' saved successfully!')],
                                                          text_align = ft.TextAlign.CENTER),
                                        actions = [ft.TextButton("OK",
                                                                 on_click = lambda e: page.close(success_dialog)
                                                                 )
                                                    ]
                                        )

        field_error_dialog = ft.AlertDialog(icon = ft.Icon(ft.Icons.ERROR_OUTLINED,
                                                     color = ft.Colors.RED),
                                            title = ft.Text("Error Saving Contact",
                                                            text_align = ft.TextAlign.CENTER),
                                            content = ft.Text("Please check input fields for errors.",
                                                                text_align= ft.TextAlign.CENTER),
                                            actions = [ft.TextButton("OK",
                                                                    on_click = lambda e: page.close(field_error_dialog)
                                                                    )
                                                        ]
                                                    )

        input_required_dialog = ft.AlertDialog(icon = ft.Icon(ft.Icons.ERROR_ROUNDED,
                                                                color = ft.Colors.RED),
                                               title = ft.Text("Error Saving Contact",
                                                                text_align = ft.TextAlign.CENTER, ),
                                               content = ft.Text("All fields are required.",
                                                                text_align= ft.TextAlign.CENTER),
                                               actions = [ft.TextButton("OK",
                                                                        on_click = lambda e: page.close(input_required_dialog)
                                                                        )
                                                         ]
                                              )

        system_error_dialog = ft.AlertDialog(icon = ft.Icon(ft.Icons.ERROR_SHARP,
                                                            color = ft.Colors.RED),
                                             title = ft.Text("Error Saving Contact"),
                                             content = ft.Text("An unexpected error occured. Please try again later.",
                                                               text_align = ft.TextAlign.CENTER),
                                             actions = [ft.TextButton('OK',
                                                                      on_click = lambda e: page.close(system_error_dialog)
                                                                      )
                                                        ]
                                            )

        if name_input.error_text or phone_input.error_text or email_input.error_text:
            page.open(field_error_dialog)
            page.update()
            return

        if not (name_input.value and phone_input.value and email_input.value):
            page.open(input_required_dialog)
            page.update()
            return

        inputs = (name_input, phone_input, email_input)

        try:
            add_contact(page, inputs, contacts_list_view, db_conn)
            page.open(success_dialog)

        except Exception:
            page.open(system_error_dialog)

        page.update()


    # ------------------------- UI COMPONENTS -------------------------

    # ------------------------- Search Bar -------------------------
    search_field = ft.Ref[ft.TextField]()
    search_icon = ft.Ref[ft.IconButton]()
    close_icon = ft.Ref[ft.IconButton]()

    def search_toggle(show : bool):
        search_field.current.visible = show
        search_icon.current.visible = not show
        close_icon.current.visible = show
        page.update()

    search_header = ft.Container(content = ft.Row([ft.Text("Contacts",
                                                            size = 30,
                                                            weight = ft.FontWeight.BOLD,
                                                            color = ft.Colors.BLACK),

                                                ft.IconButton(icon = ft.Icons.SEARCH,
                                                            ref = search_icon,
                                                            icon_size = 24,
                                                            icon_color = ft.Colors.BLUE_900,
                                                            width = 40,
                                                            on_click = lambda e: search_toggle(True),
                                                            tooltip = "Search Contacts"
                                                            ),

                                                ft.IconButton(icon = ft.Icons.CLOSE,
                                                                ref = close_icon,
                                                                icon_size = 24,
                                                                icon_color = ft.Colors.BLUE_900,
                                                                visible = False,
                                                                tooltip = "Close Search",
                                                                on_click = lambda e: search_toggle(False),
                                                                style = ft.ButtonStyle(alignment = ft.alignment.center_right))],

                                                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN),
                                                    margin = ft.Margin(5, 0, 5, 0))

    searchbox_row = ft.Container(content = ft.Row([ft.TextField(ref = search_field,
                                                                visible = False,
                                                                autofocus = True,
                                                                height = 40,
                                                                expand = True,
                                                                border_radius = 7,
                                                                border_color = ft.Colors.BLUE_900,
                                                                hint_text = "Search by name, phone, or email",
                                                                hint_style = ft.TextStyle(color = ft.Colors.BLACK),
                                                                text_style = ft.TextStyle(size = 15, color = ft.Colors.BLACK),
                                                                content_padding = ft.Padding(10, 10, 10, 10),
                                                                text_align = ft.TextAlign.START,
                                                                on_blur = lambda e: search_toggle(False),
                                                                on_change = lambda e: display_contacts(page,
                                                                                                        contacts_list_view.content,
                                                                                                        db_conn,
                                                                                                        e.control.value)),
                                                ], alignment = ft.MainAxisAlignment.END),
                                                   margin = ft.Margin(5, 0, 5, 0),
                                                )

    # -------------------- Gredients --------------------
    grad_light = ft.LinearGradient(begin = ft.alignment.center_left,
                                                      end = ft.alignment.center_right,
                                                      colors = ["#8dcefa", "#ffffff"],
                                                      tile_mode= ft.GradientTileMode.MIRROR)

    grad_dark = ft.LinearGradient(begin = ft.alignment.center_left,
                                                      end = ft.alignment.center_right,
                                                      colors = ["#0a74ff", "#7de1ff"])

    # ------------------------- Header -------------------------
    def theme_toggle(e):

        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            sw.thumb_icon = ft.Icons.LIGHT_MODE
            sw.label = "Light Mode"
            sw.tooltip = "Switch to Dark Mode"
            app_header.gradient = grad_light
            contact_list_cont.gradient = grad_light

        else:
            sw.thumb_icon = ft.Icons.DARK_MODE
            page.theme_mode = ft.ThemeMode.DARK
            sw.label = "Dark Mode"
            sw.tooltip = "Switch to Light Mode"
            app_header.gradient = grad_dark
            contact_list_cont.gradient = grad_dark

        page.update()

    sw = ft.Switch(thumb_icon = ft.Icons.LIGHT_MODE,
                   inactive_track_color = 'white',
                   active_track_color = 'black',
                   on_change = theme_toggle,
                   tooltip = "Switch to Dark Mode",
                   height = 25,
                   label = "Light Mode  ",
                   label_style = ft.TextStyle(size = 12,
                                              weight = ft.FontWeight.BOLD,
                                              color = ft.Colors.BLACK),
                   label_position = ft.LabelPosition.LEFT,
                   )

    theme_button = ft.Container(content = sw,
                                alignment = ft.alignment.bottom_right,
    )

    app_header = ft.Container(content = ft.Column([theme_button,
                                                ft.Text(f"Contact Book App",
                                                size = (page.window.width / 15) + 1,
                                                expand_loose = True,
                                                weight = ft.FontWeight.BOLD,
                                                color = ft.Colors.BLACK)],
                                                adaptive = True),

                          alignment = ft.alignment.top_center,
                          padding = ft.Padding(10, 10, 10, 10),
                          expand = True,
                          gradient = grad_light,
                          border_radius = 15,
                          height = 125,
                          margin = 0,
                          )

    # ------------------------- Contacts List View -------------------------
    contacts_list_view = ft.Container(expand = True,
                                      margin = 0,
                                      height = page.window.height - 100,
                                      content = ft.Column([],
                                      scroll = ft.ScrollMode.ALWAYS))

    add_button = ft.ElevatedButton(text = "Save Contact",
                                   on_click = lambda e: add_contact_click(e),
                                   width = 150,
                                   )

    input_fields = ft.Column(controls = [name_input,
                                         phone_input,
                                         email_input,
                                         add_button,
                                       ft.Container(height = 10)],
                            spacing = 10,
                            expand = True,
                            width = page.window.width - 100,
                            alignment = ft.MainAxisAlignment.CENTER,
                            horizontal_alignment = ft.CrossAxisAlignment.CENTER
                           )

    contact_details_cont = ft.Container(content = ft. Column([ft.Text("New Contact",
                                                                        size = page.window.width / 20,
                                                                        weight = ft.FontWeight.W_700,
                                                                        text_align = ft.TextAlign.CENTER,
                                                                        expand_loose = True,
                                                                        ),
                                                            input_fields],
                                                            alignment = ft.MainAxisAlignment.CENTER,
                                                            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                                            expand = True,
                                                            width = page.window.width - 50,
                                                            ),
                                                            alignment = ft.alignment.center,
                                                            margin = 0,
                                                            padding = ft.Padding(0, 10, 10, 0),
                                                            )

    contact_list_cont = ft.Container(content = ft.Column([search_header,
                                                          searchbox_row,
                                                          contacts_list_view]),
                                                        padding = ft.Padding(10, 10, 10, 10),
                                                        expand = True,
                                                        gradient = grad_light,
                                                        border_radius = 15,
                                                        margin = 0
                                                        )

    # ------------------------- Main Page -------------------------
    main_page = ft.Container(content = ft.Column([
                                                app_header,
                                                contact_details_cont,
                                                contact_list_cont],
                                                scroll = ft.ScrollMode.ADAPTIVE,
                                                expand = True,
                                                alignment = ft.MainAxisAlignment.START),
                            expand = True,
                            padding = ft.Padding(10, 10, 10, 10)
                            )

    display_contacts(page, contacts_list_view.content, db_conn)

    page.add(main_page)

if __name__ == "__main__":
    ft.app(target = main, assets_dir = "week4_labs/contact_book_app/src/assets")