# Python-Scraper

To manage the libraries or packages you've used and installed in your Django project, you can use `pip` (Python's package installer) along with a `requirements.txt` file. Here's how to do it:

### 1. **Create a `requirements.txt` file**

- To list all the installed packages in your Django project, you can create a `requirements.txt` file by running the following command in your terminal:
  ```bash
  pip freeze > requirements.txt
  ```
- This command will generate a `requirements.txt` file that lists all the packages you've installed with `pip`, along with their versions.

### 2. **Include the `requirements.txt` file in your project**

- Make sure to include the `requirements.txt` file in your version control system (like Git) so that it can be shared across different devices or with other developers.

### 3. **Installing packages on a new device**

- When you switch to a new device or set up your Django project on another machine, you can install all the required packages by running:
  ```bash
  pip install -r requirements.txt
  ```
- This command reads the `requirements.txt` file and installs all the listed packages.

### 4. **Virtual Environments (Optional but recommended)**

- It's a good practice to use a virtual environment to manage your project's dependencies separately from other Python projects on your machine.
- You can create a virtual environment with:
  ```bash
  python -m venv myenv
  ```
- Activate the virtual environment:
  - On Windows:
    ```bash
    myenv\Scripts\activate
    ```
  - On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```
- After activating the virtual environment, you can install packages using `pip`, and they will be isolated to your project.

### 5. **Updating `requirements.txt` after installing new packages**

- Whenever you install a new package, remember to update your `requirements.txt` file by running:
  ```bash
  pip freeze > requirements.txt
  ```

This approach ensures that your Django project's dependencies are well-managed and easily transferable across different devices, similar to how `npm` manages dependencies in Node.js projects.

### 6. Run the app

- Create a new project

```bash
python -m venv myenv
myenv\Scripts\activate
django-admin startproject < project_name >
python manage.py startapp < app_name >
```

- Alternatively you can use Pipfile to manage your dependencies

to install all your dependencies:

```bash
pipenv install
```

when installing a new dependencies:

```bash
pipenv install < package_name >
```

- Activate your Virtual Environment

```bash
myenv\Scripts\activate
```

and then migrate your SQL files

```bash
python manage.py makemigrations
python manage.py showmigrations
python manage.py migrate
```

- Run your app

```bash
python manage.py runserver
```

- To create a Django Super User

```bash
python manage.py createsuperuser
```
