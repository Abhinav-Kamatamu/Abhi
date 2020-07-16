Functioning = True
output = []

def Decrypt(Arg):
        i = 0
        
        
        global output
        while i < len(Arg):
            
            if Arg[i] == " ":
                i += 1
                output.append(" ")
                pass
            if Arg[i:(i + 3)] == "#*#":
                output.append("a")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "!_!":
                output.append("b")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "@#$":
                output.append("c")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "&*^":
                output.append("d")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "%%_":
                output.append("e")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "/^/":
                output.append("f")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "!&#":
                output.append("g")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "&!@":
                output.append("h")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "_^%":
                output.append("i")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "%_^":
                output.append("j")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "/@@":
                output.append("k")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "?<>":
                output.append("l")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "[@[":
                output.append("m")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "&!>":
                output.append("n")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "#*%":
                output.append("o")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "@*$":
                output.append("p")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "^^!":
                output.append("q")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "%>>":
                output.append("r")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "*^>":
                output.append("s")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "^*$":
                output.append("t")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "*@!":
                output.append("u")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "$$>":
                output.append("v")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "_#%":
                output.append("w")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "&%<":
                output.append("x")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "@&#":
                output.append("y")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "[[@":
                output.append("z")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "[{<":
                output.append("1")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "}]>":
                output.append("2")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "[<}":
                output.append("3")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "}>]":
                output.append("4")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "<[>":
                output.append("5")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "{<]":
                output.append("6")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "}>}":
                output.append("7")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "><}":
                output.append("8")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == ">[>":
                output.append("9")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "><]":
                output.append("0")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "!!!":
                output.append("!")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "~~~":
                output.append("~")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "```":
                output.append("`")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "@@@":
                output.append("@")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "###":
                output.append("#")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "$$$":
                output.append("$")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "%%%":
                output.append("%")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "^^^":
                output.append("^")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "&&&":
                output.append("&")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "***":
                output.append("*")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "(((":
                output.append("(")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == ")))":
                output.append(")")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "---":
                output.append("-")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "___":
                output.append("_")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "+++":
                output.append("+")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "===":
                output.append("=")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "{{{":
                output.append("{")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "}}}":
                output.append("}")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "[[[":
                output.append("[")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "]]]":
                output.append("]")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == ":::":
                output.append(":")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == ";;;":
                output.append(";")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "|||":
                output.append("|")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "'''":
                output.append("'")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == '""':
                output.append('"')
                i += 3
                
                pass
            if Arg[i:(i + 3)] == ">>>":
                output.append(">")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "<<<":
                output.append("<")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "...":
                output.append(".")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == ",,,":
                output.append(",")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "///":
                output.append("/")
                i += 3
                
                pass
            if Arg[i:(i + 3)] == "???":
                output.append("?")
                i += 3
                
                pass
            

        print("".join(output)) 

def Encrypt(Arg):

    global output

    i = 0

    while i < len(Arg):
        
        if Arg[i] == " ":
            output.append(" ")
            i += 1
            pass
        elif Arg[i] == "a":
            output.append("#*#")
            i += 1
            pass
        elif Arg[i] == "b":
            output.append("!_!")
            i += 1
            pass
        elif Arg[i] == "c":
            output.append("@#$")
            i += 1
            pass
        elif Arg[i] == "d":
            output.append("&*^")
            i += 1
            pass
        elif Arg[i] == "e":
            output.append("%%_")
            i += 1
            pass
        elif Arg[i] == "f":
            output.append("/^/")
            i += 1
            pass
        elif Arg[i] == "g":
            output.append("!&#")
            i += 1
            pass
        elif Arg[i] == "h":
            output.append("&!@")
            i += 1
            pass
        elif Arg[i] == "i":
            output.append("_^%")
            i += 1
            pass
        elif Arg[i] == "j":
            output.append("%_^")
            i += 1
            pass
        elif Arg[i] == "k":
            output.append("/@@")
            i += 1
            pass
        elif Arg[i] == "l":
            output.append("?<>")
            i += 1
            pass
        elif Arg[i] == "m":
            output.append("[@[")
            i += 1
            pass
        elif Arg[i] == "n":
            output.append("&!>")
            i += 1
            pass
        elif Arg[i] == "o":
            output.append("#*%")
            i += 1
            pass
        elif Arg[i] == "p":
            output.append("@*$")
            i += 1
            pass
        elif Arg[i] == "q":
            output.append("^^!")
            i += 1
            pass
        elif Arg[i] == "r":
            output.append("%>>")
            i += 1
            pass
        elif Arg[i] == "s":
            output.append("*^>")
            i += 1
            pass
        elif Arg[i] == "t":
            output.append("^*$")
            i += 1
            pass
        elif Arg[i] == "u":
            output.append("*@!")
            i += 1
            pass
        elif Arg[i] == "v":
            output.append("$$>")
            i += 1
            pass
        elif Arg[i] == "w":
            output.append("_#%")
            i += 1
            pass
        elif Arg[i] == "x":
            output.append("&%<")
            i += 1
            pass
        elif Arg[i] == "y":
            output.append("@&#")
            i += 1
            pass
        elif Arg[i] == "z":
            output.append("[[@")
            i += 1
            pass
        elif Arg[i] == "1":
            output.append("[{<")
            i += 1
            pass
        elif Arg[i] == "2":
            output.append("}]>")
            i += 1
            pass
        elif Arg[i] == "3":
            output.append("[<}")
            i += 1
            pass
        elif Arg[i] == "4":
            output.append("}>]")
            i += 1
            pass
        elif Arg[i] == "5":
            output.append("<[>")
            i += 1
            pass
        elif Arg[i] == "6":
            output.append("{<]")
            i += 1
            pass
        elif Arg[i] == "7":
            output.append("}>}")
            i += 1
            pass
        elif Arg[i] == "8":
            output.append("><}")
            i += 1
            pass
        elif Arg[i] == "9":
            output.append(">[>")
            i += 1
            pass
        elif Arg[i] == "0":
            output.append("><]")
            i += 1
            pass
        elif Arg[i] == "~":
            output.append("~~~")
            i += 1
            pass
        elif Arg[i] == "`":
            output.append("```")
            i += 1
            pass
        elif Arg[i] == "!":
            output.append("!!!")
            i += 1
            pass
        elif Arg[i] == "@":
            output.append("@@@")
            i += 1
            pass
        elif Arg[i] == "#":
            output.append("###")
            i += 1
            pass
        elif Arg[i] == "$":
            output.append("$$$")
            i += 1
            pass
        elif Arg[i] == "%":
            output.append("%%%")
            i += 1
            pass
        elif Arg[i] == "^":
            output.append("^^^")
            i += 1
            pass
        elif Arg[i] == "&":
            output.append("&&&")
            i += 1
            pass
        elif Arg[i] == "*":
            output.append("***")
            i += 1
            pass
        elif Arg[i] == "(":
            output.append("(((")
            i += 1
            pass
        elif Arg[i] == ")":
            output.append(")))")
            i += 1
            pass
        elif Arg[i] == "{":
            output.append("}}}")
            i += 1
            pass
        elif Arg[i] == "[":
            output.append("]]]")
            i += 1
            pass
        elif Arg[i] == "}":
            output.append("}}}")
            i += 1
            pass
        elif Arg[i] == "]":
            output.append("]]]")
            i += 1
            pass
        elif Arg[i] == "/":
            output.append("///")
            i += 1
            pass
        elif Arg[i] == "|":
            output.append("|||")
            i += 1
            pass
        elif Arg[i] == ":":
            output.append(":::")
            i += 1
            pass
        elif Arg[i] == ";":
            output.append(";;;")
            i += 1
            pass
        elif Arg[i] == "'":
            output.append("'''")
            i += 1
            pass
        elif Arg[i] == '"':
            output.append('"""')
            i += 1
            pass
        elif Arg[i] == ">":
            output.append(">>>")
            i += 1
            pass
        elif Arg[i] == "<":
            output.append("<<<")
            i += 1
            pass
        elif Arg[i] == ".":
            output.append("...")
            i += 1
            pass
        elif Arg[i] == "+":
            output.append("+++")
            i += 1
            pass
        elif Arg[i] == "=":
            output.append("===")
            i += 1
            pass
        elif Arg[i] == "-":
            output.append("---")
            i += 1
            pass
        elif Arg[i] == "_":
            output.append("___")
            i += 1
            pass

    print("".join(output))

while Functioning:

    output = []
    
    inputtype = int(input())
    
    if inputtype == 2 :
        Functioning = False
        break

    inputword = str(input())

    if inputtype == 0:
        Encrypt(inputword.lower())

    elif inputtype == 1:
        Decrypt(inputword.lower())