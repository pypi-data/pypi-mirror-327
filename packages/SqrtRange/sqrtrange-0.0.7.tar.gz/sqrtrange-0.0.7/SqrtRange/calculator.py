import math
import logging
import time
from multiprocessing import Pool

#Multiprocessing guide took from https://www.run.ai/guides/distributed-computing/parallel-computing-with-python

def Calculate(startingnumber, endingnumber, logFile, doClearLogFile, doTimeTaken):
    numbercounter = 0
    if doTimeTaken:
        starttimer = time.time()
    if doClearLogFile:
        with open(logFile, 'w'):
            pass #We write blank to clear the log file
    else:
        pass
    # Initialize logging
    logging.basicConfig(level=logging.DEBUG, filename=logFile, filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    
    for i in range(startingnumber, endingnumber+1):
        try:
            log_message = "Current number: " + str(i) + " sqrt: "+ str(math.sqrt(i))
            print(log_message)
            numbercounter = numbercounter + 1
            logging.info(log_message)
        except ValueError:
            log_message = "Invalid number for sqrt function: " + str(i)
            print(log_message)
            logging.info(log_message)
    if doTimeTaken:
        time_count = time.time() - starttimer
        print(str(time_count)+"s "+str(numbercounter-1))

def CalculateWithThreads(startingnumber, endingnumber, logFile, doClearLogFile, doTimeTaken, threads):
    with Pool(int(threads)) as p:
        p.apply(Calculate, args=(startingnumber, endingnumber, logFile, doClearLogFile, doTimeTaken))

def CalculateWOLoggingWithThreads(startingnumber, endingnumber, doTimeTaken, threads):
    with Pool(int(threads)) as p:
        p.apply(CalculateWOLogging, args=(startingnumber, endingnumber, doTimeTaken))

def CalculateWOLogging(startingnumber, endingnumber, doTimeTaken):
    numbercounter = 0
    if doTimeTaken:
        starttimer = time.time()
    for i in range(startingnumber, endingnumber+1): # We use starting number and ending number to indicate the start and the end
            try:
                log_message = "Current number: " + str(i) + " sqrt: "+ str(math.sqrt(i))
                print(log_message)
                numbercounter = numbercounter + 1
            except ValueError: # In case it's negative
               log_message = "Invalid number for sqrt function: " + str(i)
               print(log_message)
    if doTimeTaken:
        time_count = time.time() - starttimer
        print(str(time_count)+"s "+str(numbercounter-1))
