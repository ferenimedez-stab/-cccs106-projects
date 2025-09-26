# CCCS 106 Projects
Application Development and Emerging Technologies
Academic Year 2025-2026

## Student Information
- **Name:** Fernanne Hannah A. Enimedez
- **Student ID:** 231002274
- **Program:** Bachelor of Science in Computer Science
- **Section:** A

## Repository Structure

### Week 1 Labs - Environment Setup and Python Basics
- `week1_labs/hello_world.py` - Basic Python introduction
- `week1_labs/basic_calculator.py` - Simple console calculator

### Week 2 Labs - Git and Flet GUI Development
- `week2_labs/hello_flet.py` - First Flet GUI application
- `week2_labs/personal_info_gui.py` - Enhanced personal information manager
- `week2_labs/enhanced_calculator.py` - GUI calculator (coming soon)

### Week 3 Labs - Flet User Login Application Development
- `week3_labs/main.py` - User Login Form application with MySQL database integration

### Week 4 Labs - Flet User Login Application Development
- `week4_labs/main.py` - Contact Book application with SQLite database integration

### Module 1 Final Project
- `module1_final/` - Final integrated project (TBD)

## Technologies Used
- **Python 3.8+** - Main programming language
- **Flet 0.28.3** - GUI framework for cross-platform applications
- **Git & GitHub** - Version control and collaboration
- **VS Code** - Integrated development environment

## Development Environment
- **Virtual Environment:** cccs106_env_enimedez
- **Python Packages:** flet==0.28.3
- **Platform:** Windows 10/11

## How to Run Applications

### Prerequisites
1. Python 3.8+ installed
2. Virtual environment activated: `cccs106_env_enimedez\Scripts\activate`
3. Flet installed: `pip install flet==0.28.3`

### Running GUI Applications
1. Open `week2_labs` folder in File Explorer.

2. In the address bar, type in `cmd` and enter.

3. Run applications using the following commands:
    - python hello_flet.py

    - python personal_info_gui.py

### Running User Login Application
1. Open `cccs106-projects` folder in File Explorer.

2. In the address bar, type in `cmd` and enter.

3. Activate virtual environment using the command:
    - cccs106_env_enimedez\Scripts\activate

4. Move to `userlogin` directory by the entering:
    - `cd week3_labs\userlogin`

5. Run app using the command:
    - flet run
    - Note: Ensure your MySQL server is running and the fletapp database exists before running the app.

### Running Contact Book Application

1. Open the `cccs106-projects` folder in File Explorer.

2. In the address bar, type in `cmd` and press **Enter**.

3. Activate the virtual environment using the command:
   - `cccs106_env_enimedez\Scripts\activate`

4. Move to the `contact_book_app` directory by entering:
   - `cd week4_labs\contact_book_app`

5. Run the app using the command:
   - [As desktop app] `flet run`
   - [As web app] `flet run --web`
   - [As android app] `flet run --android`