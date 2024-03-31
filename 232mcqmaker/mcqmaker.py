#importing essential libraries 
import PyPDF2
import re
import random

#establishing menu variables
Banner_art = '''
  ／l、    <(Welcome to the CSE 232 MCQ generator! Made by yours truly.)         
（ﾟ､ ｡ ７         
  l  ~ヽ       
  じしf_,)ノ
'''
Banner_instructions = "* You can enter as many sample exams as you want to generate your own mcq.\n* When prompted to repeat, use Y or y to continue and N or n to stop.\n* Afterwards you'll have a txt file in your current folder with the exam!\n"




#establishing essential functions
#function to open pdf files and get pointer back 
def open_file():
    #establishing essential local variables 
    file_name = None #file name that user will input
    fp = None #file pointer

    #while loop to ask user for file to open
    while(True):
        #prompt user to enter file name 
        file_name = input("Enter valid file name: ")
        try:
            fp = open(file_name, "rb")
            #return file pointer 
            return fp
        except:
            #when the file name is not valid
            print("File is not in directory. Try again.")

#function to get the questions and answers in a dictionary with strings as keys and lists as values
def question_collection(fp):
    #establishing essential variables 
    reader = PyPDF2.PdfReader(fp) #establishing reader
    text = [] #pdf details will be added to this list line by line 
    question_dict = dict() #establishing empty dictionary, will be filled with questions later
    pastzero = 0 #counter to make sure that the cover page is skipped over in for loop later 
    #parsing through the pdf 
    for page_num in range(len(reader.pages)):
        page = (reader.pages[page_num])
        text.append(page.extract_text())

    #printing text results (debug)
    #print(text[1])
        
    #establisning essential vars for the loop below 
    question_list = list()
    answer_list = list() #this will be list of lists
    option_list = list() #will be indexes in answer list

    #parsing through the pages and adding questions to dictionary
    for page in text:
        #checking if it is past the cover page
        if(pastzero == 1):
            #code to be added
            #establishing essential variables 
            question = '' #empty string to have question added to 
            answer = '' #empty string to have answer added to
            on_question = False
            pattern = r'^\d+\.' #expression pattern used to check indexes in upcoming list
            page_list = page.split('\n') #splitting contents of the page using newline as delimiter to parse line by line

            #going through each index of page list, appending pairs to the dictionary
            for index in page_list:
                #conditional statement to determine if index is on a question prompt or not 
                if(re.match(pattern, index)):
                    on_question = True #true if the index starts with an integer followed by a period
                    #checking value of option list
                    if(option_list != []):
                        answer_list.append(option_list) #add option list to list of answers overall
                    option_list = list() #reset value of option list
                    answer = ''
                #checks if index is start of new answer
                try:
                    if(index[0] == '('):
                        option_list.append(answer) #add previous answer to list of options for specific question
                        question_list.append(question) #append the question prompt
                        question = '' #reset val of question 
                        on_question = False #not on question anymore
                        answer = ''
                except:
                    pass
                
                #appending lines to the answer and question strings 
                if(on_question == True):
                    question += index
                else:
                    answer += index


            #debug
            #print(page_list) 
        else:
            pastzero += 1 #increment the counter by 1 to indicate it is past the first page
    
    #after the loop
    filtered_question_list = [x for x in question_list if x != ''] #empty list that will have questions added to it without '' indexes 

    #making a dictionary with questions as keys and lists of options as values 
    for index, prompt in enumerate(filtered_question_list):
        if(index != (len(filtered_question_list) - 1)):
            question_dict[prompt] = answer_list[index]

    
    #return the dictionary
    #print(question_dict) debug 
    return question_dict

    
#main function
def main():
    #establishing essential variables 
    dict_list = list() #init list that will have dictionaries of exams in them
    user_continue = None #var for user input 

    #printing the banner
    print(Banner_art)
    print(Banner_instructions)

    #while loop asking for file names
    while(True):
        #prompt user for fp
        fp = open_file()
        dict_to_add = question_collection(fp)
        dict_list.append(dict_to_add)

        #asks if user wanna continue 
        user_continue = input("Do you want to enter in another sample exam? (y/n)")
        if(user_continue.lower() == 'n'):
            #if user says no break the loop
            break
    
    #generating the mcq
    with open('mcq.txt', 'w') as file:
        #code here
        #iterates through each dicitonary and chooses 7 random problems to write on the generated mcq
        for index in dict_list:
            #print(index) debug
            key_list = list(index.keys())
            value_list = list(index.values())
            for i in range(7):
                #choose random index 
                index = random.randint(0, len(key_list))
                #write the question prompt down
                file.write('\n' + key_list[index] + "\n")
                #writing the questions down
                for question in value_list[index]:
                    file.write('\n' + question)
        
    #thank you message
    cat = '''⠀⠀⠀⠀⠀⣴⠉⡙⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠤⣚⡯⠴⢬⣱⡀⠀
    ⠀⠀⠀⠀⢰⡇⣷⡌⢲⣄⡑⢢⡀⠀⠀⠀⠀⠀⢠⠾⢋⠔⣨⣴⣿⣷⡌⠇⡇⠀
    ⠀⠀⠀⠀⢸⢹⣿⣿⣄⢻⣿⣷⣝⠷⢤⣤⣤⡶⢋⣴⣑⠟⠿⠿⠿⣿⣿⡀⡇⠀
    ⠀⠀⠀⠀⢸⢸⣿⡄⢁⣸⣿⣋⣥⣶⣶⣶⣶⣶⣶⣿⣿⣶⣟⡁⠚⣿⣿⡇⡇⠀
    ⢀⣠⡤⠤⠾⡘⠋⢀⣘⠋⠉⠉⠉⠉⢭⣭⣭⣭⣍⠉⢩⣭⠉⠉⠂⠙⠛⠃⣇⡀
    ⠏⠀⠀⢿⣿⣷⡀⠀⢿⡄⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣆⠀⢿⣇⠀⠀⠀⠀⠀⠀⠈⢱
    ⣦⠀⠀⠈⢿⣿⣧⠀⠘⣿⠀⠀⠀⡀⠀⠀⠘⣿⣿⣿⣿⡆⠀⢻⡆⠀⠀⠀⠀⠀⠀⢸
    ⢻⡄⠀⠀⠘⠛⠉⠂⠀⠙⠁⠀⣼⣧⠀⠀⠀⠈⠀⠀⠈⠙⠀⠘⠓⠀⠀⠀⠀⠀⢀⡟
    ⠀⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⣏⠀
    ⠀⠀⠛⢶⢰⣶⢢⣤⣤⣄⠲⣶⠖⠀⣙⣀⠀⠀⠀⠤⢤⣀⣀⡀⣀⣠⣾⠟⡌⠀
    ⠀⠀⠀⠘⢄⠃⣿⣿⣿⣿⠗⠀⠾⢿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⠸⠟⣡⣤⡳⢦
    ⠀⠀⠀⠀⠀⢻⡆⣙⡿⢷⣾⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿⡿⠟⢡⣴⣾⣿⣿⣿⣦
    ⠀⠀⠀⠀⠀⡼⢁⡟⣫⣶⣍⡙⠛⠛⠛⠛⠛⣽⡖⣉⣠⣶⣶⣌⠛⢿⣿⣿⣿⣿
    ⠀⠀⠀⢀⠔⢡⢎⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠹⣿⣿⣿
    ⠀⢠⠖⢁⣴⡿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢹⣿⣿'''
    print(cat)
    print("Thank you so much for using this! My discord is akrdude if you want to connect or give feedback! ♡")

main()

#fp = open_file()
#question_collection(fp)