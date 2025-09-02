# Lab 2 Report: Git Version Control and Flet GUI Development

**Student Name:** Fernanne Hannnah A. Enimedez
**Student ID:** 231002274
**Section:** A
**Date:** September 2, 2025

## Git Configuration

### Repository Setup
- **GitHub Repository:** https://github.com/ferenimedez-stab/-cccs106-projects.git
- **Local Repository:** ✅ Initialized and connected
- **Commit History:** 7 (including the latest) commits with descriptive messages

### Git Skills Demonstrated
- ✅ Repository initialization and configuration
- ✅ Adding, committing, and pushing changes
- ✅ Branch creation and merging
- ✅ Remote repository management

## Flet GUI Applications

### 1. hello_flet.py
- **Status:** ✅ Completed
- **Features:** Interactive greeting, student info display, dialog boxes
- **UI Components:** Text, TextField, Buttons, Dialog, Containers
- **Notes:**
    - Student information displayed in the application can be modified in the source code.
    - The UI elements are not responsive.
    - In the <i>Interactive Section</i>, there are no input constraints: integers and special characters are accepted and treated as strings.

### 2. personal_info_gui.py
- **Status:** ✅ Completed
- **Features:** Form inputs, dropdowns, radio buttons, profile generation
- **UI Components:** TextField, Dropdown, RadioGroup, Containers, Scrolling
- **Error Handling:** Input validation and user feedback
- **Notes:**
    - The UI elements are not responsive.
    - Input field errors are not indicated.
    - Invalid input in the Age field nullifies profile generation.
    - All other fields accept integers and special characters.
    - Clicking the <i>Clear Form</i> button resets all input fields, but retains previous dropdown selections.
        - However, this is a frontend issue: if a new selection is not made, no input is registered on the backend.

## Technical Skills Developed

### Git Version Control
- Understanding of repository concepts
- Basic Git workflow (add, commit, push)
- Branch management and merging
- Remote repository collaboration

### Flet GUI Development
- Flet 0.28.3 syntax and components
- Page configuration and layout management
- Event handling and user interaction
- Modern UI design principles

## Challenges and Solutions

During this activity, I encountered minimal difficulties, thanks to the lesson I carried over from the previous lab where I realised the importance of reading instructions carefully and following along step by step.

### Multi-line git commit
One specific issue occurred when I was working with a commit command that contained a multi-line description:

    git commit -m "Add Week 2 labs: Flet GUI applications

    - hello_flet.py: Basic Flet introduction with interactive elements
    - personal_info_gui.py: Enhanced personal information manager with GUI
    - Both applications use Flet 0.28.3 syntax and modern UI components"

I misread the command and mistakenly added only the first line, ending it with what I thought was an omitted closing quotation mark. When I tried the same commands again by copy-pasting, the terminal treated each line individually. I solved this mishap by removing the line breaks and rewriting the command in a single line, separating phrases with spaces. Fortunately, the mistakes made did not affect the repository in any way.

### Flet attribute issue
For Exercise 2.2, where we create two basic Flet applications, VS Code flagged certain attributes: `page.dialog` and `age.value`.


`page.dialog` had the error message:

    Cannot assign to attribute "dialog" for class "Page" Attribute "dialog" is unknown Pylance (reportAttributeAccessIssue)

![page.dialog error](/week2_labs/lab2_screenshots/page.dialog%20error.png)

The initial attempt to troubleshoot this issue, I researched and concluded that this was caused by how Pylance performs type checking. Since Flet uses dynamic attributes that are not always declares in the type stubs Pylance relies on, VS code flags them despite being valid at runtime.

However, upon revisiting the code, I noticed that the function for the `App info` button were neatly defined, which meant the issue wasn't caused by missing logic. This led me to a deeper investigation, where I confirmed that the `page.dialog = dialog` approach had been deprecated in the current version of Flet installed (v0.28.3).

The correct approach is to append the dialog to the page's overlay:

![page.dialog error - FIXED](/week2_labs/lab2_screenshots/page.dialog%20error%20-%20FIXED.png)

As for the `.value` property, the initial conclusion stands. This means that it exists and works fine at runtime, Pylance does not always recognise it.

![.value warning](/week2_labs/lab2_screenshots/age.value%20warning.png)

To address this, the code can be updated to explicitly cast the value before converting it to an integer:

![.value warning - FIXED](/week2_labs/lab2_screenshots/age.value%20warning%20-%20FIXED.png)

This small change relieves the type-cast warning without affection the app's functionalities.

## Learning Outcomes

In this activity, we were introduced to the basic flow of Git version control. While I am still in the process of fully grasping its practice, I have started to understand some of its core commands.

At this stage, I can perform tasks such as adding new files to the staging area, committing changes, pushing them to the main branch, and checking the commit logs.

Initially, I was not aware of what the staging area represent until upon writing this. From what I understand, the staging area can be likened to a <i>waiting room</i> where changes are placed before they are officially committed. This allows developers to carefully choose which changes to include in each commit.

On another note, collaborative programming practices involve numerous confusing commands. Nevertheless, I can see how version control is essential in team projects as it encourages proper organisation of codes and assets, makes it possible to track change history, and provides a structured was to monitor project development.

In terms of GUI development, I realised some editor warnings (like Flet and Pylance) don't always indicate a bugged program - they sometimes only reflect how a framework handles attributes differently from what the static analyser expects. Moreover, I found working with Flet to be intuitive and visually appealing.

## Screenshots

### Git Repository
- **GitHub repository with commit history**
    ![GitHub repository with commit history](/week2_labs/lab2_screenshots/GitHub%20Repo%20with%20commit%20history.png)

- **Local git log showing commits**
    ![Local git log showing commits](/week2_labs/lab2_screenshots/local%20git%20log%20of%20commits.png)

### GUI Applications
- **hello_flet.py running with all features**
    ![hello_flet.py running with all features](/week2_labs/lab2_screenshots/Hello%20Flet.png)

- **personal_info_gui.py with filled form and generated profile**
    ![personal_info_gui.py with filled form and generated profile](/week2_labs/lab2_screenshots/Personal%20Information%20GUI.png)

## Future Enhancements

### Hello Flet Application
- **Responsive UI:** Wrap forms and controls in expandable containers so they resize with the viewport.
- **Input Constraints and Validation:** Enforce field types or patterns, and display inline errors before or on submission.
- **Modifiable Student Information:** Add a toggle for viewing and editing modes with save/cancel actions.

### Personal Information Application
- **Responsive UI:** Wrap forms and controls in expandable containers so they resize with the viewport.
- **Input Field Error Indicators:** Add real-time red boarders or icons, error summary banner, or inline messages after a failed submission.
- **Robust Input Constraints and Validation:** Adopt client- and server-side checks, age/unit ranges, or contextual tooltips.
- **Reset Dropdown Selection:** Ensure <i>Clear Form</i> resets all input and selections; optionally prompt an "Are you sure?" dialog and sync reset with the backend.