# The action for the 'intro/calculator' route.
from django.shortcuts import render
from django.core.context_processors import csrf
# Create your views here.
num = ["1","2","3","4","5","6","7","8","9","0"]
opt = ["+","-","*","/"]
eql = "="
clear="C"
save = 0
flag=False
mark=False
format_flag=False;
def home(request):
    if request.method=="GET":
        context = {"display": 0, "preval": 0, "preopt": "+", "curval": 0, "error": 0}
        return render(request, "calculator/calculator.html", context)
    if request.method=="POST":
        try:
            for key in request.POST.keys():
                if key =="number":
                    if isNum(request.POST[key]):
                      context = updateVal(request, request.POST[key])
                    else:
                      print "before"+str(flag)
                      flag=False
                      context = {"display": "InvalidInput", "preval": 0, "preopt": "+", "curval": 0, "error": 0}
                elif key=="operator":
                    if isOperator(request.POST[key]):
                        context = updateOpt(request, request.POST[key])
                    else:
                        context = {"display": "InvalidInput", "preval": 0, "preopt": "+", "curval": 0, "error": 0}
                elif key=="clear":
                    if request.POST[key]=="C":
                        context=init();
                    else:
                        context = {"display": "InvalidInput", "preval": 0, "preopt": "+", "curval": 0, "error": 0}
                elif key == "equal":
                    if request.POST[key]=="=":
                        context = computeResult(request, key)
                    else:
                        context = {"display": "InvalidInput", "preval": 0, "preopt": "+", "curval": 0, "error": 0}
            return render(request, "calculator/calculator.html", context)
        except Exception:
            context= context = {"display": "InvalidInput", "preval": 0, "preopt": "+", "curval": 0, "error": 0}
            return render(request, "calculator/calculator.html", context)
def updateVal(request, val):
        preVal = request.POST["preval"]
        curVal = request.POST["curval"]
        preOpt = request.POST["preopt"]
        global flag
        flag=False
        if request.POST["display"]=="Error" or request.POST["preval"]=="Error":
            print "here"
            preVal="0"
            curVal="0"
            preOpt="+"
        print "display: "+request.POST["display"]
        if curVal == "0":
            curVal = val
        elif len(curVal) < 19:
            curVal += val
        print "after update value "+str(preVal)+" "+str(curVal)+" "+str(preOpt)
        context = {"preval": preVal, "curval": curVal, "preopt": preOpt, "display": curVal}
        return context

def updateOpt(request, key):
    preVal = request.POST["preval"]
    curVal = request.POST["curval"]
    preOpt = request.POST["preopt"]
    if request.POST["display"]=="Error" or request.POST["preval"]=="Error":
         preVal=0
         curVal=0
         preOpt="+"
         print "befor update operator1 "+str(preVal)+" "+str(curVal)+" "+str(preOpt)
    else:
         if preOpt !="0":
             preVal = compute(preVal, curVal, preOpt, save)
             print "befor update operator "+"preval:"+str(preVal) +" curval:" +str(curVal)+" "+str(preOpt)
         if preVal == "Error":
            print "hello"
            context = error();
         else:
              curVal = 0
              preOpt = key
              print "after update operator in Else"+"preval:"+str(preVal) +" curval:" +str(curVal)+" "+str(preOpt)
    context = {"preval": preVal, "curval": curVal, "preopt": preOpt, "display": preVal}
    return context;

def computeResult(request, key):
    preVal = request.POST["preval"]
    curVal = request.POST["curval"]
    preOpt = request.POST["preopt"]
    print "compute result"+preVal+" "+curVal+" "+preOpt
    print request.POST["display"]
    global save
    global flag
    if request.POST["display"]=="Error" or request.POST["display"]=="InvalidInput":
        context =init()
        print "befor update operator1 "+str(preVal)+" "+str(curVal)+" "+str(preOpt)
        return context
    else:
        res = compute(preVal, curVal, preOpt, save)
        if res == "Error":
                context = error();
        else:
                preVal = 0
                curVal = 0
                preOpt = "+"
                flag=True;
                save = res
                print str(preVal)+" "+str(curVal)+" "+str(preOpt)
                context = {"preval": preVal, "curval": curVal, "preopt": preOpt, "display": res}
        return context;

def compute(preVal, curVal, opt,save):
    if isNum(str(preVal)) and isNum(str(curVal)) and isNum(str(save)):
        print "in compute: "+str(preVal)+" "+str(curVal)+" "+str(opt)+str(flag)
        res = 0
        if flag:
            if opt == "+" and flag:
                res = int(save) + int(curVal)
            elif opt == "-" and flag:
                res = int(save) - int(curVal)
            elif opt == "*" and flag:
                res = int(save) * int(curVal)
            elif opt == "/" and flag:
                try:
                    res = int(save) / int(curVal)
                except ZeroDivisionError:
                    res = "Error"
            print "special"+str(preVal)+" "+str(curVal)+" "+str(opt)
        else:
            if opt == "+":
                    res = int(preVal) + int(curVal)
            elif opt == "-":
                    res = int(preVal) - int(curVal)
            elif opt == "*":
                    res = int(preVal) * int(curVal)
            elif opt == "/":
                    try:
                        res = int(preVal) / int(curVal)
                    except ZeroDivisionError:
                        res = "Error"
        return res
    else:
        return "Error"

def init():
    flag = False
    return {"display": 0, "preval": 0, "preopt": "+", "curval": 0, "error": 0}

def error():
    flag = False
    return {"error" : 1, "display" : "Error","preval": 0, "preopt": "+", "curval": 0,}

def isNum(value):
    try:
        value=int(value)
        return isinstance(value,int)
    except ValueError:
        return False
#    return value.isdigit()
#    print "is Num: "+value
#    print "is num return false"

def isOperator(opt):
       if opt=="+" or opt=="-" or opt=="*" or opt=="/" or opt=="=" or opt=="C":
           return True
       else:
           return False
