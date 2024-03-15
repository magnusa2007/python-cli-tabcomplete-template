import sys
from msvcrt import getch

#add you tabs here
tab = dict()
def getTabs():
    global tab
    tab['+/-/*/"/"'] = ['+','-','*','/']
        
getTabs()
history = []

def write(str):
    sys.stdout.write(str)
    sys.stdout.flush()
    
def tabInput(b):
    index = 0
    line = ''
    sys.stdout.write('\0337') #save location
    while True:
        sys.stdout.write('\0338') #load location
        sys.stdout.write('\033[2K') #clear line
        write(b+line)
        key = str(getch())[2:-1]
        if len(key) == 1:
            line = line+key
            
        elif key == '\\r':
            print()
            history.append(line)
            index = 0
            return line
        
        elif key == '\\x08':
            line = line[0:-1]
        
        elif key == '\\xe0':
                key = str(getch())[2:-1]
                try:
                    if key == 'H': #up
                        index-=1
                        line = history[index%len(history)]
                    elif key == 'P': #down
                        index+=1
                        line = history[index%len(history)]
                    
                except:
                    pass
                    
        elif key == '\\t': #the magic tab complete coded at 12 pm
            try:
                split = line.split()
                if len(split) == 1:
                    for i in command:
                        if i[0:len(split[0])].lower() == split[0].lower():
                            line = i
                else:
                    if split[-1] in tab[command[split[0]]['args'][len(split)-2]]:
                        i = tab[command[split[0]]['args'][len(split)-2]][(tab[command[split[0]]['args'][len(split)-2]].index(split[-1])+1)%len(tab[command[split[0]]['args'][len(split)-2]])]
                        string=''
                        for s in split[0:-1]:
                           string = string+' '+s
                        line = string[1:]+' '+i
                    else:
                        for i in tab[command[split[0]]['args'][len(split)-2]]:
                            if i[0:len(split[-1])].lower() == split[-1].lower():
                                string=''
                                for s in split[0:-1]:
                                   string = string+' '+s
                                line = string[1:]+' '+i
                                break
            except:
                pass

def help(cmds='all'):
    if cmds == 'all':
        for cmd in command:
            print(f'{cmd}:\n  Arguments:\n    {str(command[cmd]["args"])}\n  Description:\n    {command[cmd]["des"]}\n')
    elif cmds in command:
        cmd = cmds
        print(f'{cmd}:\n  Arguments:\n    {str(command[cmd]["args"])}\n  Description:\n    {command[cmd]["des"]}\n')
    else:
        print('Unkown Command')

#Your commands
def math(n1,f,n2):
    n1,n2 = int(n1),int(n2)
    if f=='+':
        print(n1+n2)
    elif f=="-":
        print(n1-n2)
    elif f=="*":
        print(n1*n2)
    elif f == "/":
        print(n1/n2)


#Commands
command = dict()
command['help'] = {'args':['command'],'des': 'Show all the commands.','f':help}

#Add info for your commands here
command['math'] = {'args':['number1','+/-/*/"/"','number2'],'des': 'Does some MATH','f':math}
command['exit'] = {'args':['errorcode'],'des': 'Goodbye','f':exit}


command = dict(sorted(command.items()))

def commandHandle(input):
    cs = input.split(' ')
    if cs[0] in command:
        for c in cs[1:]:
            try:
                if not c in tab[command[cs[0]]['args'][cs.index(c)-1]]:
                    print(f'{c} is not a {command[cs[0]]["args"][cs.index(c)-1]}')
                    return False
            except:
                pass
            
        command[cs[0]]['f'](*cs[1:])
    else:
        print('Unkown command do help for list of all commands')
        
while True:
    getTabs()
    input = tabInput('> ')
    commandHandle(input)
