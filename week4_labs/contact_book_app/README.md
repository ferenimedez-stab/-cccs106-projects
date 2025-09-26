# ContactBookApp app
This is a contact manager application built with **Flet** and **SQLite**.

- **Status:** ✅ Completed
- **Features:**
  - Add, edit, delete, and search contacts
  - Alphabetical grouping with dividers
- **UI Components:**
  - Card (contact list)
  - CircleAvatar
  - TextField (Name, Phone, Email)
  - Elevated Button (Save Contact)
  - PopupMenuButton (Edit, Delete)
  - IconButton (Call)
  - AlertDialog (success, field error, input required error, system error, etc.)
  - Row, Column, ListView
- **Error Handling:**
  - Input validation for name, phone number and emails
  - Confirmation before deletion
- **Notes:**
  - Contact initials automatically generate from one or two names
  - The UI dynamically resizes (avatars, fonts, icons) based on screen width
  - Action buttons (Call, Edit, Delete) are always visible for quick access
  - Alphabet dividers organize contacts for easier navigation

## Run the app

Run as a desktop app:

```
flet run
```

Run as a web app:

```
flet run --web
```

Run as an android app:

```
flet run --android
```

### Poetry

Install dependencies from `pyproject.toml`:

```
poetry install
```

Run as a desktop app:

```
poetry run flet run
```

Run as a web app:

```
poetry run flet run --web
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/getting-started/).

## Build the app

### Android

```
flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).