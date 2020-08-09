#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 17:06:42 2020

@author: fahmi
"""
file=open('obj.txt','r')
obj=file.readlines()
objects=[]
folders=[]
RA=[]
Dec=[]
NH=[]

print("=======================================================================")
print("                        obj.txt file creator                           ")
print("   The aim of this program (object.py) is to create obj.txt containing ")
print(" list  of  object  including the name of  object,  folder of the data, ")
print(" position  (RA  and Dec), hydrogen column density (NH). Also, you need ")
print(" to provide the main directory of your object folders.                 ")
print("=======================================================================")
print("")
print("")
print("Below is your current obj.txt")
print("")
for i in range(len(obj)):
    print(obj[i])
    
print("Do you want to reset your obj.txt or add a/some object(s)?")
print("1. Reset my obj.txt")
print("2. Add a/some object(s)")
print("3. Please don't do anything")
opt=int(input("Input the number: "))

print("")
print("")
print("")
if opt==1:
    print("=======================================================================")
    print("                         RESETTING YOUR OBJ.TXT                        ")
    print(" *Note: If you don't have some information, please text 'null' without ")
    print(" the apostropes")
    print("=======================================================================")
    print("")
    print("Please provide /your/directory/path/  ex: /home/user/Documents/data/")
    path=str(input("PATH: "))
    print("")
    print("Please give your object(s) information.")
    j=1
    print("Object number "+str(j))
    objects.append(str(input("Please give your object's name correctly: ")))
    folders.append(str(input("Please input your object's folder (I advise you to not include space into it): ")))
    RA.append(str(input("Please input right ascension (Degree and Decimal):")))
    Dec.append(str(input("Please input declination (Degree and Decimal): ")))
    NH.append(str(input("Please input NH value (10^22 cm^-2): ")))
    op=str(input("Do you wish to add another object? (Y/N) "))
    while (op=='Y' or op=='y'):
        j+=1
        print("Object number "+str(j))
        objects.append(str(input("Please give your object's name correctly: ")))
        folders.append(str(input("Please input your object's folder (I advise you to not include space into it): ")))
        RA.append(str(input("Please input right ascension (Degree and Decimal):")))
        Dec.append(str(input("Please input declination (Degree and Decimal): ")))
        NH.append(str(input("Please input NH value (10^22 cm^-2): ")))
        op=str(input("Do you wish to add another object? (Y/N) "))
    
    print("Thank you! Your input(s) will be saved into obj.txt")
    print("Your obj.txt is updated successfully")
    
    writes=[]
    writes.append("# Swift XRT Data Reduction Input File\n")
    writes.append("#\n")
    writes.append("#===================================================\n")
    writes.append("#Please provide main directory of your objects:\n")
    writes.append(path+"\n")
    writes.append("#===================================================\n")
    writes.append("# *FolderName*  Object_Name     RA      Dec	NH(10^22 cm^-2)\n")
    for i in range(len(objects)):
        writes.append('*'+folders[i]+'*\t'+objects[i]+'\t'+RA[i]+'\t'+Dec[i]+'\t'+NH[i]+"\n")
    
    f=open('obj.txt','w')
    for i in range(len(writes)):
        f.writelines(writes[i])
    f.close()
    
if opt==2:
    print("=======================================================================")
    print("              ADDING ADDITIONAL OBJECTS INTO YOUR OBJ.TXT              ")
    print(" *Note: If you don't have some information, please text 'null' without ")
    print(" the apostropes")
    print("=======================================================================")
    print("")

    for i in range(len(obj)):
        if obj[i][0]!='\n' and obj[i][0]!='#' and obj[i][0]!='/':
            path=obj[i].split('\t')[0][1:-1]
    print("Please give your object(s) information.")
    j=1
    print("Object number "+str(j))
    objects.append(str(input("Please give your object's name correctly: ")))
    folders.append(str(input("Please input your object's folder (I advise you to not include space into it): ")))
    RA.append(str(input("Please input right ascension (Degree and Decimal):")))
    Dec.append(str(input("Please input declination (Degree and Decimal): ")))
    NH.append(str(input("Please input NH value (10^22 cm^-2): ")))
    op=str(input("Do you wish to add another object? (Y/N) "))
    while (op=='Y' or op=='y'):
        j+=1
        print("Object number "+str(j))
        objects.append(str(input("Please give your object's name correctly: ")))
        folders.append(str(input("Please input your object's folder (I advise you to not include space into it): ")))
        RA.append(str(input("Please input right ascension (Degree and Decimal):")))
        Dec.append(str(input("Please input declination (Degree and Decimal): ")))
        NH.append(str(input("Please input NH value (10^22 cm^-2): ")))
        op=str(input("Do you wish to add another object? (Y/N) "))
    
    print("Thank you! Your input(s) will be saved into obj.txt")
    print("Your obj.txt is updated successfully")
    
    writes=[]
    writes.append("# Swift XRT Data Reduction Input File\n")
    writes.append("#\n")
    writes.append("#===================================================\n")
    writes.append("#Please provide main directory of your objects:\n")
    writes.append(path+"\n")
    writes.append("#===================================================\n")
    writes.append("# *FolderName*  Object_Name     RA      Dec	NH(10^22 cm^-2)\n")
    for i in range(len(objects)):
        writes.append('*'+folders[i]+'*\t'+objects[i]+'\t'+RA[i]+'\t'+Dec[i]+'\t'+NH[i]+'\n')
    
    f=open('obj.txt','w')
    for i in range(len(writes)):
        f.writelines(writes[i])
    f.close()
    
if opt==3:
    print("It is okay. You will exit this program. Enjoy the automation.")

o=str(input("Do you wish to start your automation? (Y/N) "))
if o=='Y' or o=='y':
    import main.py
elif o=='N' or o=='n':
    print('BYE!')
    
