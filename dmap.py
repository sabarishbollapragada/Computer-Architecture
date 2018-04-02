import math as math

while 0 == 0:
    result1 = []
    result2 = []
    print("Cache model")
    print("1. 32KB")
    print("2. 16KB + 16KB")
    model = input("Choose a model: ")
    if int(model) == 1:
        cacheSize = 32768
    elif int(model) == 2:
        cacheSize = 16384

    blockSize = input("Please enter the block size: ")

    arraySize = int(cacheSize)/int(blockSize)
    indexSize = int(math.log(arraySize,2))
    if int(model) == 1:
        cache = [0]*int(arraySize)
        missCount = 0
        hitCount = 0
    elif int(model) ==2:
        cache1 = [0]*int(arraySize)
        cache2 = [0]*int(arraySize)
        missCount1 = 0
        hitCount1 = 0
        missCount2 = 0
        hitCount2 = 0

    print("Reading file")
    with open("trace.din") as infile:
        for line in infile:
            result1.append(line.split(' ')[0])
            result2.append(line.split(' ')[1])
        infile.closed
    if int(model) == 1:
        i=0
        while i<len(result2):
        
            hexValue = result2[i]
            i = i+1
            binStr = str(bin(int(hexValue, 16))[2:].zfill(32))
            tag = int(binStr[:20],2)
    
            index = int(binStr[20:20+indexSize],2)
            modIndex = index%int(arraySize)
            if cache[modIndex] == 0:
                cache.insert(modIndex, tag)
                missCount = missCount + 1
            elif cache[modIndex] == tag:
                hitCount = hitCount + 1
            elif tag != cache[modIndex]:
                missCount = missCount + 1
                cache.insert(modIndex, tag)

        print("Miss Count -- "+ str(missCount))
        print("Hit Count -- "+ str(hitCount))
	missCount=float(missCount)
	hitCount=float(hitCount)
	missrate=float((missCount/(missCount+hitCount)))
	print("Miss rate -- "+str(round(missrate, 4))+"\n\n")
    elif int(model) == 2:
        i=0 
        while i<len(result2):
            opCode = result1[i]
            opCode = int(opCode)
            hexValue = result2[i]
            i = i+1
            if opCode == 0 or opCode == 1:
                binStr = str(bin(int(hexValue, 16))[2:].zfill(32))
                tag = int(binStr[:20],2)
            
                index = int(binStr[20:20+indexSize],2)
                modIndex = index%int(arraySize)
                if cache1[modIndex] == 0:
                    cache1.insert(modIndex, tag)
                    missCount1 = missCount1 + 1
                elif cache1[modIndex] == tag:
                    hitCount1 = hitCount1 + 1
                elif tag != cache1[modIndex]:
                    missCount1 = missCount1 + 1
                    cache1.insert(modIndex, tag)

           
            elif opCode == 2:
                binStr = str(bin(int(hexValue, 16))[2:].zfill(32))
                tag = int(binStr[:20],2)
            
                index = int(binStr[20:20+indexSize],2)
                modIndex = index%int(arraySize)
                if cache2[modIndex] == 0:
                    cache2.insert(modIndex, tag)
                    missCount2 = missCount2 + 1
                elif cache2[modIndex] == tag:
                    hitCount2 = hitCount2 + 1
                elif tag != cache2[modIndex]:
                    missCount2 = missCount2 + 1
                    cache2.insert(modIndex, tag)

        print("Data Cache Miss Count -- "+ str(missCount1))
        print("Data Cache Hit Count -- "+ str(hitCount1))
	missCount1=float(missCount1)
	hitCount1=float(hitCount1)
	missrate1=float((missCount1/(missCount1+hitCount1)))
	print("Miss rate -- "+str(round(missrate1, 4)))
        print("Instructions Cache Miss Count -- "+ str(missCount2))
        print("Instructions Cache Hit Count -- "+ str(hitCount2))
	missCount2=float(missCount2)
	hitCount2=float(hitCount2)
	missrate2=float((missCount2/(missCount2+hitCount2)))
	print("Miss rate -- "+str(round(missrate2, 4))+"\n\n")
            
