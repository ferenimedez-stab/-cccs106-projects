# Userlogin app
This is a simple user login application built with **Flet** with **MySQL**.

- **Status:** ✅ Completed
- **Features:**
  - User authentication with MySQL
  - Secure password input with reveal option
  - Login validation with feedback dialogs
- **UI Components:**
  - TextField (username, password)
  - ElevatedButton (login)
  - AlertDialog (success, failure, input error, database error)
  - Container, Column, Icons
- **Error Handling:**
  - Empty input detection for username and password
  - Invalid credentials detection
  - Database connection error handling
- **Notes:**
  - Frameless window with custom size and styling
  - Username and age fields are not included — strictly username/password login

## Run the app

Run as a desktop app:

```
flet run
```

Run as a web app:

```
flet run --web`
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