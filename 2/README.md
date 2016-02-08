In ningw/homework/2/, it includes:
    webapps/
        settings.py
        urls.py
        [etc.]
    calculator/
        static/
            calculator/
                calculator.css
            images/
        templates/
            calculator/
                calculator.html
        urls.py
        views.py
        models.py
        [etc.]
    manage.py
    db.sqlite3
    README.md
****************************************************************************************************************
How to use this simple calculator?
The normal operations which are required in the write up are not list here.I list several another cases which I
deal with.

Case1: 
First, you could click one number randomly, it will display the number you just click.
Then, you could click a operator such as "+","-","*","/".
Then,you could click another number and click the operator "=",then you will get the result.
Then, There are three situations which you could choose:
    1: you could still click operator such as "+","-","*","/", it will calculate on the basis
    of your last calculation result.
    2: you could click a number randomly, then click an operator and continue your calculation.This operation
    just like restart a new computation.
    3:If click the button "C",it will initialize this calculator.

Case2:
First you could click a number randomly,then click the operator "/", then click the "0" button, it will display a
hint "error".Now,if you click a number,it will restart a calculation, you could do calculation what you want.If
you click the operator such as "+","-","*","/" or "C",the display will be set zero.You also could do a new
calculation. 

Case:Input Exception
If you change the value or name of the button tag to a wrong format value in the calculator.html,it will display
a hint "InvalidInput".

****************************************************************************************************************
Some situations which I do not fix.
If you click the "/" button two consecutive times, it will display a hint "Error".You could choose reload the
main page into a initial state or click the C button clear the display and restart the calculations.
When you test the wrong format input and get the hint "InvalidInout", you need to click the "C" button,then you
could start a new calculation.

If you enter corner case, you could reload the mian page,then you could do your calculations again.


    