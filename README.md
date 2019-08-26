- Navigate to local directory
- export FLASK_APP="".py
- export FLASK_DEBUG=1


- @app.route("/")
    - This is a route
    - It is a decoration (something fancy that handles the backend work)
    - It takes in a "directory" as an arguement (the directory is the last part of a link on the website's browser)

- render_template("page_name.html", args)
    - This is a flask function that renders HTML templates
    - It can take various arguements
    - It can handle multiple arguements that can serve as variables
    - When it takes in variables, those variables can be accessed from the respective HTML page
        - In order to script in python on that HTML page, you need to use {%____%}

- Inheritance
    - In Flask, the concept of inheritance pertains to the reduction of writing code
    - When developing pages, often times there are reused components
    - Inheritance uses this to create 1 main template as the parent
    - The other pages that utilize this template will be children
    - The children will inherit the parent's core html and will display that as well
    - The children can then have their own modifications in a specified area mentioned in the parent's code block
    - Its purpose is to reduce writing code

- Databases
    - SQLAlchemy will be used
    - It is great as an ORM (Object Relational Mapper)
    - It allows us to use different databases at different points in development
        - Development = SQLite, Production = Posgres etc...
        - It allows us to switch between database types seamlessly
    - pip install flask-sqlalchemy