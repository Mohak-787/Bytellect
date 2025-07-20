# Bytellect: A Modern Flask Quiz Platform

#### Developed by: Mohak Devkota

#### CS50 Final Project – 2025

---

## Introduction

**Bytellect** is a fully responsive and interactive quiz web application developed using Python's **Flask** framework. The platform provides users with a seamless quiz-taking experience across three unique game modes—**Rapid**, **Survival**, and **Standard**—each offering its own challenge and pacing. The goal of the project was to merge aesthetic design with functional web development to create a platform that is both educational and engaging. Designed with scalability and user experience in mind, Bytellect leverages modern UI patterns such as **glassmorphism**, server-enforced timers, and dynamic modals for an intuitive and secure user journey.

This project was created for the final project of CS50, Harvard University’s Introduction to Computer Science. It aims to demonstrate proficiency in backend logic, frontend responsiveness, state management, and the integration of multiple technologies to produce a cohesive full-stack application.

---

## Project Overview

Bytellect allows users to register, log in, and choose between different quiz modes. In **Rapid Mode**, users answer questions against a strict timer that continues even if the user refreshes or navigates away. **Survival Mode** gives users only one attempt—if they answer a question incorrectly, the quiz ends immediately. **Standard Mode** offers a traditional quiz experience with no time pressure or life constraints.

All user-sensitive operations such as logout, password change, and account deletion are handled with confirmation modals to prevent accidental actions. The entire interface is styled using custom CSS, incorporating both Bootstrap’s responsive grid system and modern aesthetics like blur effects, shadowing, and clean color schemes for an immersive user experience.

---

## Design Philosophy

The design of Bytellect focuses on both **functionality and security**. One of the key architectural decisions was to enforce the quiz timer on the **server side** rather than relying purely on JavaScript. This ensures fairness and eliminates potential exploits, like refreshing the page to reset the timer.

The decision to use **modals** for sensitive actions was driven by UX best practices—preventing accidental data loss and enhancing the sense of control for users. Additionally, the UI layout is designed with **mobile-first responsiveness**, ensuring that the experience remains consistent across all devices.

From a software engineering perspective, the app adheres to the **separation of concerns** principle. All logic resides in the backend (`app.py`), the structure and layout in the HTML templates, the styling in the CSS file, and interactivity in JavaScript. This modularity makes the project maintainable and scalable.

---

## File Structure and Responsibilities

```
bytellect/
├── app.py              # Main Flask application and routing logic
├── requirements.txt    # Python dependencies for the project
├── quiz.db             # SQLite database storing users, questions, and quiz data
├── static/
│   ├── style.css       # Custom CSS for layout, responsiveness, and theming
│   └── script.js       # JavaScript for modals and rapid mode timer
├── templates/
│   ├── layout.html     # Base HTML template extended by all other pages
│   ├── index.html      # Landing page (welcome, login/register prompts)
│   ├── dashboard.html  # Dashboard for selecting quiz modes
│   ├── quiz.html       # Core quiz interface (renders questions and handles logic)
│   ├── profile.html    # Displays user info and access to settings
│   └── settings.html   # Account settings (password change, delete, logout)
└── README.md           # Complete project documentation
```

### `app.py`

This is the heart of the application. It handles all Flask routes, manages user sessions, and controls quiz logic. It provides functionality for registering and logging in users (using hashed passwords), initiating quiz sessions, validating answers, and updating progress. It also calculates and tracks time for Rapid Mode server-side, to ensure consistent and cheat-resistant timing.

### `requirements.txt`

This file lists all Python dependencies required to run the application, including Flask, Werkzeug, and Jinja2. It allows for consistent environment setup across machines using `pip install -r requirements.txt`.

### `quiz.db`

This is the SQLite database file that stores all persistent data for the application. It contains tables for quiz questions, user accounts, and potentially user progress or scores. The `app.py` backend interacts with `quiz.db` to fetch quiz questions, validate answers, and manage user authentication and profile information.

- **Typical tables include:**
  - `users`: Stores user credentials (with hashed passwords), profile details, and registration timestamps.
  - `question`: Stores quiz questions, answer options, and the correct answer for each question.

You can modify the quiz content or user data by editing `quiz.db` using a tool like DB Browser for SQLite or the SQLite command-line interface. If the database does not exist, the application may create it and initialize the required tables on first run, or you can provide a pre-populated `quiz.db` file in your project directory.

### `static/style.css`

Contains all custom styling used throughout the application. It includes responsive design features, glassmorphism effects (such as background blur and transparency), and UI components like cards and buttons. Special attention was given to maintaining readability and contrast, even on complex backgrounds.

### `static/script.js`

Provides JavaScript functionalities including countdown logic for Rapid Mode, and modal control for logout and account deletion confirmations. The script updates the timer every second on the client-side and ensures clean interaction patterns like clicking outside to close modals.

### `templates/layout.html`

This base template is extended by all other pages. It includes the navigation bar, footer, and references to Bootstrap, CSS, and JS files. It defines the layout skeleton so that other templates can inject their specific content using Jinja’s `{% block content %}`.

### `templates/index.html`

The landing page for unauthenticated users. It introduces the platform and provides links to log in or register. The visual design includes a welcoming hero section with branding and call-to-action buttons.

### `templates/dashboard.html`

After logging in, users land here. It presents the three quiz modes, each with descriptions and start buttons. This page serves as the central hub for navigating quiz functionalities.

### `templates/quiz.html`

This template dynamically renders each quiz question and answer choices. It includes real-time timer display (in Rapid Mode), feedback for correct/incorrect answers, and navigation for submitting and advancing through the quiz.

### `templates/profile.html`

Displays user-specific information such as username, full name, email, and membership duration. It includes a section for account settings, with links to password change and account deletion.

### `templates/settings.html`

Consolidates all user management features—password change, account deletion, and logout—under a clean and accessible layout. Modals are used for confirmation to prevent accidental actions.

---

## Final Thoughts

Bytellect reflects the culmination of many topics taught throughout CS50: web development with Flask, data handling via sessions, secure user authentication, and frontend interactivity using JavaScript. It blends logic and aesthetics to create a project that is not only functional but enjoyable to use.

This project challenged me to think about real-world concerns like user security, interface responsiveness, and server-client data synchronization. It also pushed me to write cleaner, more modular code and to develop a user-first design mindset. Overall, Bytellect represents my growth as a developer and stands as a proud submission for my final CS50 project.

---

## Acknowledgements

I would like to extend my deepest thanks to the entire **CS50 team**, especially Professor **David J. Malan**, for delivering such an intellectually rich and inspiring course. The structure and content of CS50 provided the foundation and motivation for this project, and I’m truly grateful for the learning journey.

Special thanks also go to:

* The **Flask** documentation and community for their comprehensive guides and troubleshooting help.
* The **Bootstrap** team for providing a responsive and accessible frontend framework.
* My friends who provided feedback during development and UI testing.

---

## License

This project was created for educational purposes and submitted as a final project for CS50.
© 2025 Mohak Devkota. All rights reserved.

---
