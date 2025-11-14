## Skill badges
![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
# About project
In this course, I learned Django ORM, the main way to work with data in Django. I learned more about models and their mapping to the database, migrations, and query construction. I figured out how to describe the relationships between models and perform reversible operations in transaction mode.
### Topics to be considered:
* Working with a modern ORM;
* Build complex queries with aggregation and annotation functions;
* Analyze the effectiveness of using ORM
### Installation
The __poetry__ project manager must be installed to work with the project
```
git clone https://github.com/NoFate35/django-orm.git
cd django-orm
poetry install
```
### Description
The project is managed by the poetry project manager and consists of several applications: 
* libruary - In this test, a library system with the functions of issuing books and calculating statistics is implemented;
* quote - The Quote model describes a collection of quotations from works of popular culture.  The "Quote of the day" is selected using the class method;
* shop - This task implements a system for counting items in the shopping cart, sorting, and using F() -expressions.

__Testing has been conducted__

