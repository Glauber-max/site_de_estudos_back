# site de estudos
é o back end do site, a proposta é ser um site de estudos com algumas features importantes para produtividade, um projeto pessoal e academico

the project starts in "main.py", actually i create the database with sqlalchemy for transform command SQL in class from python(for easy change database),the directory models are all tables, and also in conecctions (src.database.conecctions) are all
script for create a database

the primary function add is "create user", the code open a router create user, get name, email and password, check if email exists in database, if not exists, after other verification stole in database and send email for user, after user send token the code active a account, so user can use the account

feature until now -> create account(and send token for activate account)