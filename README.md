# Christian Dating App Backend


## Description
A Django-based backend for a Christian dating app designed to help Christians mingle and find companionship. The backend handles user authentication, matchmaking, profile management, discovery of new matches, application settings, and chat functionalities.

## Features
- User Authentication (userauth)
- Matchmaking (matches)
- Profile Management (profiles)
- Discovery of New Matches (discover)
- Application Settings Management (appsettings)
- Chat (chatapp)

## Installation

### Prerequisites
- Python 3.x
- Django 3.x
- PostgreSQL (or any preferred database)

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/SamuelMaiko/dating-app.git
    ```

2. Navigate to the project directory:
    ```bash
    cd dating-app
    ```

3. Create a virtual environment and activate it:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. [Set up the environment variables](#environment-configuration)

6. Set up the database:
    - **For development purposes**, you can use SQLite. Ensure your `settings.py` file has the following configuration commented/uncommented accordingly:
        ```python
        # settings.py

        #Use this for development with SQLite

         DATABASES = {
             'default': {
                 'ENGINE': 'django.db.backends.sqlite3',
                 'NAME': BASE_DIR / 'db.sqlite3',
             }
         }

        #Use this for production with PostgreSQL

        # DATABASES = {
        #    'default': {
        #        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #        'NAME': config('DATABASE_NAME'),
        #        'USER': config('DATABASE_USER'),
        #        'PASSWORD': config('DATABASE_PASSWORD'),
        #        'HOST': config('DATABASE_HOST'),
        #        'PORT': config('DATABASE_PORT', default='5432'),
        #    }
        # }
        ```
        
        - **For production purposes**, configure the environment variables in your `.env` file:
        ```plaintext
        DATABASE_NAME=your_database_name
        DATABASE_USER=your_database_user
        DATABASE_PASSWORD=your_database_password
        DATABASE_HOST=your_database_host
        DATABASE_PORT=your_database_port
        ```

7. Create a superuser for admin access:
    ```bash
    python manage.py createsuperuser
    ```

8. Start the development server:
    ```bash
    python manage.py runserver
    ```

## Environment Configuration

Before running the project, you need to set up your environment variables. Follow these steps:

1. Copy the example environment variables file to create your own `.env` file:
    ```bash
    cp .env.example .env
    ```

2. Open the `.env` file in a text editor:
    In VS code 

    **OR** 

    ```bash
    nano .env  # or use any other text editor
    ```

3. Fill in your own configuration details. Here’s an explanation of each variable:

    ```plaintext
    # .env

    DEBUG=True  # Set to False in production

    # Database configuration
    DATABASE_NAME=your_database_name
    DATABASE_USER=your_database_user
    DATABASE_PASSWORD=your_database_password
    DATABASE_HOST=your_database_host
    DATABASE_PORT=your_database_port

    # Email settings
    EMAIL_BACKEND=your_email_backend
    EMAIL_HOST=your_email_host
    EMAIL_PORT=your_email_port
    EMAIL_USE_TLS=True  # or False, depending on your configuration
    EMAIL_HOST_USER=your_email_user
    EMAIL_HOST_PASSWORD=your_email_password

    # Additional settings
    ALLOWED_HOSTS=localhost,127.0.0.1  # Add your allowed hosts here
    ```

## Known Issues

### 1. Serving Images in Production
- **Description:** The application is not currently configured to serve images in a production environment.
- **Status:** Configuration pending
- **Workaround:** None currently available. Please use a local development setup for image-related features until this is added.

### 2. Real-time Messaging Not Implemented
- **Description:** Real-time messaging is not implemented due to existing bugs that are currently under investigation.
- **Status:** Investigating and seeking solutions
- **Workaround:** Users can use alternative communication methods or refresh the chat manually. Real-time messaging will be added once the issues are resolved.

### 3. Database Configuration
- **Description:** The application is still using SQLite for the database and has not been connected to a hosted database.
- **Status:** Migration to a hosted database is planned
- **Workaround:** For development purposes, SQLite is sufficient. For production, please configure a PostgreSQL database as described in the [Installation](#installation) section.


## Support and Assistance

If you have any questions about the codebase or encounter issues while working on it, feel free to reach out for assistance. Here are some ways to get support:

- **Contact:** You can reach out to [Maiko](mailto:samuel.maiko.dev@gmail.com) for assistance or clarification on any aspect of the code.
- **Documentation:** Refer to the project's documentation for guidance on setup, usage, and troubleshooting.
- **Issue Reporting:** If you encounter bugs or unexpected behavior, please report them by opening a new issue in the [GitHub Issues](https://github.com/SamuelMaiko/dating-app/issues) section of this repository. Provide as much detail as possible, including steps to reproduce the issue, your environment, and any relevant logs or screenshots.

We're here to help ensure a smooth experience with the codebase and to address any questions or concerns you may have.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
Created by [Maiko](mailto:samuel.maiko.dev@gmail.com) - feel free to contact me!