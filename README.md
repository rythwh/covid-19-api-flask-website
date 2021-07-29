![Screenshot of Website](/screenshots/COVIDWebsiteScreenshot1.png)

CIS 3210 Lab 10
Ryan White

How to start server:
1. With a terminal open in the app.py directory...
2. Run command: export FLASK_APP=app.py
3. Run command: flask run --host=0.0.0.0 --port=17628
4. Server will be running locally.

How to connect to SQL:
1. mysql -h <redacted> -u <Central Login ID> -p
2. password is student number
3. enter command: use <redacted>
5. enter command: describe users;
4. enter command: select * from users;

How to use:
1. Login or Register from the "login" page.
2. If successful, you will move through to the "users" page.
    2.1. Press "Logout" to clear your session and return to the login page.
    2.2. Press "Refresh" to refresh the data pulled from the COVID API (data is refreshed on page load anyway).