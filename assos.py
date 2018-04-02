# -*- coding: utf-8 -*-
import math as math
import random

while 0 == 0:
    result1 = []  #array for opcode
    result2 = []  #array for addresses
    print("Cache model")
    print("1. 32KB")
    print("2. 16KB + 16KB")
    model = input("Choose a model: ")
    if int(model) == 1:
        cacheSize = 32768
    elif int(model) == 2:
        cacheSize = 16384
    blockSize = input("Please enter the block size: ") 
    asso = 4
    arraySize = int(int(cacheSize)/int(blockSize)) #calculate number of blocks
    indexSize = int(math.log((arraySize),2))       #calculate the index size
    if int(model) == 1:
        #create a two dimensional array for storing the cache
        cache = [[0]*int (arraySize/asso),[0]*int (arraySize/asso),[0]*int (arraySize/asso),[0]*int (arraySize/asso)]
        #create a two dimensional array for storing the position values for lru 
        lru = [[0]*int (arraySize/asso),[0]*int (arraySize/asso),[0]*int (arraySize/asso),[0]*int (arraySize/asso)]
        missCount = 0
        hitCount = 0
    elif int(model) ==2:
        #defining two cache's and two lru's for data and instructions
        cache1 = [[0]*int (arraySize/asso),[0]*int (arraySize/asso),[0]*int (arraySize/asso),[0]*int (arraySize/asso)]
        lru1 = [[0]*int (arraySize/asso),[0]*int (arraySize/asso),[0]*int (arraySize/asso),[0]*int (arraySize/asso)]
        cache2 = [[0]*int (arraySize/asso),[0]*int (arraySize/asso),[0]*int (arraySize/asso),[0]*int (arraySize/asso)]
        lru2 = [[0]*int (arraySize/asso),[0]*int (arraySize/asso),[0]*int (arraySize/asso),[0]*int (arraySize/asso)]
        missCount1 = 0
        hitCount1 = 0
        missCount2 = 0
        hitCount2 = 0
        print("Reading file")
    with open("trace.din") as infile:  # reading the opcodes and addresses into result1 and result2 respectively
        for line in infile:
            result1.append(line.split(' ')[0])
            result2.append(line.split(' ')[1])
        infile.closed
    if int(model) == 1:  #unified cache
         i=0
         
         while i<len(result2):  #for the length of addresses
             y=0
             h=0
             
             hexValue = result2[i]   #get the address which is in hex
             
             i = i+1
             
             binStr = str(bin(int(hexValue, 16))[2:].zfill(32))  #convert it into a binary string
             
             tag = int(binStr[:20],2) #get the tag
             
             index = int(binStr[20:20+indexSize],2) #get the index
             modIndex = index%int(arraySize/asso)   #calculating the modulus of index
             
             count1 = 0
             count2 = 0
             
             for x in range(asso):           #looping in the parallel cache's 
                 if cache[x][modIndex]==0:   # for the same index value
                     h=h+1
             if h==4:                       #h gets 4 when initially all the values of cache are 0's
                 h=0
                 
                 missCount=missCount+1   
                 m=1     #get a random int for the first time
                 cache[m][modIndex]=tag    #put the tag in that random cache for that particular index value 
                 count5=m
                 while count5 < asso-1:   
                    lru[count5][modIndex]=lru[count5+1][modIndex] #move all the positions to left by one from the array position where the tag is stored
                    count5 = count5+1
                 lru[asso-1][modIndex]=m  #now put that position value into the last array element to know that it is the most recently used one
                 continue
                                      
             for l in range(asso):
                 if cache[l][modIndex] == tag:  #if we get a hit in the parallel cache's for the index value
                     
                     hitCount = hitCount + 1
                     a=l;
                     count3 = l
                     while count3 < asso-1:
                         lru[count3][modIndex]=lru[count3+1][modIndex] #move all the positions to left by one from the array position where tag is stored
                         count3 = count3+1
                         
                     lru[asso-1][modIndex]=a # now put that position value into the last array element to know that it is the most recently used
                 else:
                    y=y+1   #we count y if there is a miss 
             if y==asso:
                y=0
                
                missCount=missCount+1
                z=lru[0][modIndex]    #put the first array element which is the least used position in the cache in z 
                cache[z][modIndex]=tag #now replace that tag with the new tag
                count4=z
                while count4 < asso-1:
                    lru[count4][modIndex]=lru[count4+1][modIndex] #move all the positions to left by one from the array position where tag is stored   
                    count4 = count4+1
                lru[asso-1][modIndex]=z # now put that position value into the last array element to know that it is most recently used
                
         print("Miss Count -- "+ str(missCount))
         print("Hit Count -- "+ str(hitCount))
         missRate = float(float(missCount)/float(hitCount))
         print("Miss Rate -- "+ str(round(missRate,5))+"\n\n")
    elif int(model) == 2: #in split cache we define two 2-D arrays for data and instructions and two 2-D lru arrays to check the positions and implement the same logic as above
        i=0 
        while i<len(result2):
            y=0
            h=0
            
            opCode = result1[i] #get opcode
            opCode = int(opCode)
         
            hexValue = result2[i]  # get address
            i = i+1
            if opCode == 0 or opCode == 1: #check for data read/write
                binStr = str(bin(int(hexValue, 16))[2:].zfill(32))
             
                tag = int(binStr[:20],2)
             
                index = int(binStr[20:20+indexSize],2)
                modIndex = index%int(arraySize/asso)
             
                count1 = 0
                count2 = 0
            
                for x in range(asso):
                    if cache2[x][modIndex]==0:
                        h=h+1
                if h==4:
                    h=0
                    
                    missCount2=missCount2+1
                    m=1
                    cache2[m][modIndex]=tag
                    count5=m
                    while count5 < asso-1:
                        lru2[count5][modIndex]=lru2[count5+1][modIndex]
                        count5 = count5+1
                    lru2[asso-1][modIndex]=m
                    continue
                                      
                for l in range(asso):
                    if cache2[l][modIndex] == tag:
                        #print("In Hit 1")
                        hitCount2 = hitCount2 + 1
                        a=l;
                        count3 = l
                        while count3 < asso-1:
                            lru2[count3][modIndex]=lru2[count3+1][modIndex]
                            count3 = count3+1
                        
                        lru2[asso-1][modIndex]=a
                    else:
                        y=y+1
                if y==asso:
                    y=0
                    
                    missCount2=missCount2+1
                    z=lru2[0][modIndex]
                    cache2[z][modIndex]=tag
                    count4=z
                    while count4 < asso-1:
                        lru2[count4][modIndex]=lru2[count4+1][modIndex]
                        count4 = count4+1
                    lru2[asso-1][modIndex]=z
            elif opCode == 2:
                binStr = str(bin(int(hexValue, 16))[2:].zfill(32))
             
                tag = int(binStr[:20],2)
             
                index = int(binStr[20:20+indexSize],2)
                modIndex = index%int(arraySize/asso)
             
                count1 = 0
                count2 = 0
            
                for x in range(asso):
                    if cache1[x][modIndex]==0:
                        h=h+1
                if h==4:
                    h=0
                    
                    missCount1=missCount1+1
                    m=1
                    cache1[m][modIndex]=tag
                    count5=m
                    while count5 < asso-1:
                        lru1[count5][modIndex]=lru1[count5+1][modIndex]
                        count5 = count5+1
                    lru1[asso-1][modIndex]=m
                    continue
                                      
                for l in range(asso):
                    if cache1[l][modIndex] == tag:
                        #print("In Hit 1")
                        hitCount1 = hitCount1 + 1
                        a=l;
                        count3 = l
                        while count3 < asso-1:
                            lru1[count3][modIndex]=lru1[count3+1][modIndex]
                            count3 = count3+1
                        
                        lru1[asso-1][modIndex]=a
                    else:
                        y=y+1
                if y==asso:
                    y=0
                    #print("In Miss 2")
                    missCount1=missCount1+1
                    z=lru1[0][modIndex]
                    cache1[z][modIndex]=tag
                    count4=z
                    while count4 < asso-1:
                        lru1[count4][modIndex]=lru1[count4+1][modIndex]
                        count4 = count4+1
                    lru1[asso-1][modIndex]=z
            
            
            
            
            

        print("Data Cache Miss Count -- "+ str(missCount2))
        print("Data Cache Hit Count -- "+ str(hitCount2))
        missRate1 = float(float(missCount2)/float(hitCount2))
        print("Data Cache Miss Rate -- "+ str(round(missRate1,5)))
        print("Instructions Cache Miss Count -- "+ str(missCount1))
        print("Instructions Cache Hit Count -- "+ str(hitCount1))
        missRate2 = float(float(missCount1)/float(hitCount1))
        print("Instructions Cache Miss Rate -- "+ str(round(missRate2,5))+"\n\n")
