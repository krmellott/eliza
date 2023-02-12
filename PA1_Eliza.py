#Kyle Mellott
#9/22/2022


#This program is an Eliza style chatbot that acts as an academic advisor.
#The advisor has no extensive knowledge of academic advising, and fills
#the role by reflecting user statements back to the user in the form of a
#question.
#An example of input would be:
# -> [User] What is my GPA?
# => [Eliza] You should know your GPA.

#OR

# -> [User] Should I take 18 credits next semester?
# => [Eliza] You should focus on this semester.

#Usage begins with Eliza asking for the user's name, which must be answered
#with "My name is ____". Eliza then prompts for the user's major, and then
#the conversation begins and the user may ask whatever they wish to ask.
#The conversation will continue until the user types "exit" and hits enter.

#The steps of the program are as follows:
#   The program begins by calling welcome(), which prompts the user for their
#   name and major and stores that information in global variables.
#   The program then enters a while loop until the user enters "exit". Each iteration
#   of the loop begins with prompting for user input, passing the user input to
#   abuse_check(), which opens a text file with a series of bad words, one per line. The
#   program searches the user input for each word in the text file. If a word in the text
#   file is found in the user input, it will prompt a special message that the input is not
#   appropriate. The user input is then passed to gibberish_detect(), which checks for
#   gibberish phrases such as "aspdoifjpiaq" or "04891734". It works by searching for uncommon
#   bigrams such as 'q' without an immediate 'u', or 'df'. It also searches the string to
#   verify there is at least one vowel. Lack of a vowel would indicate gibberish. It does not
#   catch all gibberish but serves to catch a significant amount. The input is then passed to
#   keyword_check(), which checks the user input for a dictionary of key words that will result
#   in an immediate response regardless of the context or rest of the question. The keywords
#   are ranked in order of importance so that if there are multiple keywords in a sentence,
#   the most important will be responded to. The value of the most important keyword is stored
#   in the variable "max" and returned. Following the keyword_check(), if max != 0, that
#   indicates there was a keyword found, and the user_input and max is passed to keyword_handle()
#   keyword_handle() is a switch statement that prints out a predetermined message according to the
#   value in "max". If max was returned as 0, that indicates that there is no keyword in the input, and
#   the input is instead passed to script_flip(). Script_flip() uses RegEx pattern matching to determine
#   the context of the question or statement and responds by reflecting this question or statement back
#   to the user in an appropriate manner. If the user input does not match any of the patterns that the
#   program would recognize, the program responds with "Tell me more." This completes one iteration of
#   the while loop. 

import re

#A dictionary of keywords that will cause an immediate response regardless of
#the rest of the input, with weights/values assigned to each in order of importance
#Higher value words are more important
keywords = {
    'graduation': 9,
    'graduate': 9,
    'final exam': 8,
    'degree plan': 7,
    'midterm': 6,
    'major': 5,
    'grades': 3
    }

#Recieves "response" as an argument from main()
#Opens a locally stored file called "bad_words.txt"
#For each line in the file, containing one word per line,
#searches for that word in the user's reponse
def abuse_check(response):
    global name
    file = open("bad_words.txt", "r")
    check = None
    for line in file:
        check = re.search("({})".format(response), line) #Searches the response for each line
        if (check != None):
            
            #The following if statement verifies that the portion flagged as abuse
            #is the same number of characters as the word in the text file. This
            #prevents substrings from being flagged as the full bad word
            #For example, this if statement prevents "arn" being flagged as "darn"
            
            if (check.span()[1]-check.span()[0] == len(line.strip())):
                print("-> [Eliza] That's not appropriate language.")
                print("=> [" + name + "] ", end = " ")
    file.close()


#Recieves "response" as an argument from main()
#the "printed" variable insures that the response is
#only printed one time if multiple indications of gibberish are found
#This will not catch all gibberish, but will catch a significant amount
#of it
def gibberish_detect(response):
    printed = False

    #The following check searches for input without vowels, as this would
    #be an indication of gibberish
    check = re.search("[aeiou]", response)
    if (check == None):
        print("-> [Eliza] What are you trying to say?")
        printed = True
    #The next to checks search for very uncommon or impossible bigrams that
    #would likely never occur in a word, indicating that the input would be
    #gibberish
    check = re.search(".*[d][f].* | .*[a][a].* | .*[i][i].*", response)
    check = re.search(".*[j][f].* | .*[u][u].* | .*[s][j].*", response)
    check = re.search(".*[f][j].* | .*[f][p].* | .*[v][f].*", response)    
    if (check != None and printed == False):
        print("-> [Eliza] What are you trying to say?")
        printed = true

    #This check searches for an instance of a 'q' where there is not immediately a
    # 'u' after. This almost never occurs and would indicate gibberish
    check = re.search(".*[q][^u].*", response)
    if (check != None and printed == False):
        print("-> [Eliza] What are you trying to say?")

#For each word in the keywords dictionary, checks to see if that keyword is in the
#user input received. If it is in the input, the function keeps track of the keyword
#with the highest weight. It then returns the highest weight for use in a switch statement
def keyword_check(user_input):
    max = 0
    for word in keywords:
        if re.search(word, user_input) != None and keywords[word] > max:
            max = keywords[word]
    return max


#Recieves the user input from main() and the maximum weight from keyword_check()
#Uses a match-case (Python's version of a switch) statement to address each keyword
#with a statement that ignores the rest of the context
def keyword_handle(user_input, max):
    max = str(max)
    global major
    global name
    match max:
        case "9":
            print("-> [Eliza] It's too early to worry about graduation, focus on your studies.")
            print("=> [" + name + "] ", end = " ")
        case "8":
            print("-> [Eliza] Are you worried about your final exam?")
            print("=> [" + name + "] ", end = " ")
        case "7":
            print("-> [Eliza] You should know your degree plan and requirements.")
            print("=> [" + name + "] ", end = " ")
        case "6":
            print("-> [Eliza] Are you worried about your midterm?")
            print("=> [" + name + "] ", end = " ")
        case "5":
            print("-> [Eliza] Do you not like " + major + "?")
            print("=> [" + name + "] ", end = " ")
        case "3":
            print("-> [Eliza] Are you worried about your grades?")
            print("=> [" + name + "] ", end = " ")

#Welcome function creates globals "name" and "major" so that they can be
#referenced at any point in the program. Introduces the program and prompts for
#name and major, then asks if the user likes their major. This then starts the
#conversation

#Disclaimer: I've never used global variables before but this seems like the
#perfect scenario to use them in
def welcome():
    global name
    global major
    print("This is Eliza the Academic Advisor, programmed by Kyle Mellott.")
    user_input = ""
    print("-> [Eliza] Hi, I'm an academic advisor. What is your name?")
    print("=> [Unknown]", end = " ")
    user_input = input()
    check = re.search(".* name is (\w*).*", user_input)
    name = check.group(1)       #Stores name into global variable "name"
    print("-> [Eliza] Hi " + name + ". What is your major?")
    print("=> [" + name + "] ", end = " ")
    major = input()             #Stores major into global variable "major"
    print("-> [Eliza] Do you like " + major + "?")
    print("=> [" + name + "] ", end = " ")

    
#script_flip is the function that reflects user input back to the user in the form
#of a question if there are no keywords present in the input
def script_flip(user_input):
    global name
    global major
    #Searches for input of the form "I x my y" and answers with
    #"Why do you say you x your y?"
    if re.search("[I|i] (\w+) my ([\w+ ]*)[\.|,|!|?]*.*\.", user_input):        
        x = re.search("[I|i] (\w+) my ([\w+ ]*)[\.|,|!|?]*.*\.", user_input)
        print("-> [Eliza] Why do you say you " + x.group(1) + " your " + x.group(2) + "?")
        print("=> [" + name + "] ", end = " ")
        
    #Searches for "I'm worried about x" and answers with "Why are you worried about x?"
    elif re.search("I'm worried about (.*).*", user_input):
        x = re.search("I'm worried about (.*).*", user_input)
        print("-> [Eliza] Why are you worried about " + x.group(1) + "?")
        print("=> [" + name + "] ", end = " ")
    
    #Searches for "Can I ask ...." and responds with "Of course, I'm here to help"
    #Meant to catch phrases like "Can I ask a question?"
    elif re.search(".*[C|c]an I ask .*", user_input):
        print("-> [Eliza] Of course, I'm here to help.")
        print("=> [" + name + "] ", end = " ")
        
    #Searches for "What is|are my x" and responds with "You should know your x"
    #Meant to catch phrases like "What is my GPA" or "What are my graduation requirements?"
    elif re.search(".*\. What [\w+]* my ([\w+ ]*)?", user_input):
        x = re.search("What [\w+]* my ([\w+ ]*)?", user_input)
        print("-> [Eliza] You should know your " + x.group(1) + ".")
        print("=> [" + name + "] ", end = " ")

    #Searches for "I don't feel like x" and responds with "Why don't you feel like x?"    
    elif re.search("I don't feel like I ([\w+ ]*)[\.|,|!|?]*.*\.", user_input):
        x = re.search("I don't feel like I ([\w+ ]*)[\.|,|!|?]*.*\.", user_input)
        print("-> [Eliza] Why don't you feel like you " + x.group(1) + "?")
        print("=> [" + name + "] ", end = " ")

    #Searches for "How many x do I y?" and answers with "You should know how many x you y"
    #Meant to catch phrases like "How many credits do I need to graduate?"
    elif re.search("How many (\w*) do I (\w*).*", user_input):
        x = re.search("How many (\w*) do I (\w*).*", user_input)
        print("-> [Eliza] You should know how many " + x.group(1) + " you " + x.group(2) + ".")
        print("=> [" + name + "] ", end = " ")

    #Searches for "Is x difficult?" and responds with "I think you'll be able to handle x."
    elif re.search("Is (/w*) difficult?", user_input):
        x = re.search("Is (/w*) difficult?", user_input)
        print("-> [Eliza] I think you'll be able to handle " + x.group(1) + ".")
        print("=> [" + name + "] ", end = " ")

    #Searches for any questions about next semester and responds with
    #"You should focus on this semester."
    elif re.search(".* next semester?", user_input):
        x = re.search(".* next semester?", user_input)
        print("-> [Eliza] You should focus on this semester.")
        print("=> [" + name + "] ", end = " ")
        
    #Searches for "I don't feel like x" and responds with "Why do you say you don't feel like x?"
    elif re.search(".* I don't feel like (\w*).*", user_input):
        x = re.search(".* I don't feel like (\w*).*", user_input)
        print("-> [Eliza] Why do you say you don't feel like " + x.group(1) + "?")
        print("=> [" + name + "] ", end = " ")      
        


    #If the input does not match any of the expected formats, reponds with "Tell me more."
    #This is a general response to help keep the conversation moving.
    else:
        if (user_input != "exit"):
            print("-> [Eliza] Tell me more.")
            print("=> [" + name + "] ", end = " ")
        
        


#MAIN FUNCTION - Calls all other functions
#Creates "while" loop to continue conversation until users enters "exit"
def main():
    welcome()
    user_input = ""   
    while user_input != "exit":
        user_input = input()
        abuse_check(user_input)
        gibberish_detect(user_input)
        max = keyword_check(user_input)
        if max != 0:
            keyword_handle(user_input, max)
        else:
            script_flip(user_input)
        
        

#Used to launch the main() function upon running the program
if __name__ == '__main__':
    main()


        
    
