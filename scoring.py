# Formulas to map random ranged numbers to a range from 1 to 5

def scoring(x,min,max,inverse):
    #If corpora range is single digit then the errors and sentences are automatically best(to avoid div-by-0)
    if max==min:
        return 5
    else:
        y=((x-min)/(max-min))*4 # scaling score then adjusting based on error or sentences
    # Inverse used for errors
    if(inverse): # For error
        return round(5.0-y,2)
    else: # For number of sentence
        return round(1.0+y,2)