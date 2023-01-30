Adaptive traffic light operation

Technical specification - https://docs.google.com/document/d/1I2szHeLekeMz50pSeKMdptnfu58ajlmqztLIBUm2DQc/edit

How to run (for Windows):
1. download ZIP of program from gitHub https://github.com/OleksandrNovitskyi/ATLO
2. Unpack ZIP (you should get folder ".../ATLO-views/...")
3. in comand line change directory to "ATLO-views" (...\> cd Downloads\ATLO-views)
4. Inslall virtual environment "...\> py -m venv project-name"
5. Activate the environment "...\> project-name\Scripts\activate"
6. Install Django "...\> py -m pip install Django"
7. Inslall MySQL "...\> pip install mysqlclient"
8. in comand line change directory to "ATLO-views/atlo" (...\> cd atlo)
9. Run server (...\> py manage.py runserver)
10. Open register page in browser (http://127.0.0.1:8000/main/register/)

How to use:

The main task of the program is to calculate the time of operation of the green traffic light signal in the up-down and right-left directions.

1. On register page fill in all information about you and parameters of your experiment
2. Login 
3. You can see results of calculation in the center of the screen
4. Program capabilities:
- change user - logout and register new users
- change traffic parameters and get new calculation (Buton "Calculate")
- add new experiments (rigt top angle)
- change curent experiment - activate oldest experiments
- complicate the calculation using other parameters (left bottom angle)
