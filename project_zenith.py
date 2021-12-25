#Tomek Botwicz

#Import needed packages
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, DISABLED
import string
from PIL import ImageTk, Image
import os

#Declare needed global variable (I tried to minimize them!)
global label_file_explorer

#Start user_interface
def user_interface(window):
    #Call global variable
    global label_file_explorer

    #Open and format header image
    image = Image.open('zenith_logo.png')
    image = image.resize((200, 200), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)

    #Insert image
    label = Label(window, image = photo)
    label.image = photo
    label.grid(row=1)

    #Insert text intro
    ttk.Label(window,text='Welcome to Project Zenith, an intelligent economic decision-making tool!\t').grid(column = 0, row = 2,padx = 20, pady = 5)
    ttk.Label(window,text='Inspired by Project Cybersyn, it recommends worker allocation to open posts based on personal skills and past job experience.').grid(column = 0,row = 3,padx = 20, pady = 5)
    ttk.Label(window,text='To begin, please select an import file. Each file line should be formatted as such: NAME / SKILLS (COMMA SEPARATED) / PAST JOBS (COMMA SEPARATED)').grid(column = 0,row = 4,padx = 20, pady = 5)

    #Create file opened label
    label_file_explorer = Label(window,
                            text = "File Opened: none",
                            width = 100, height = 2, font =
                            ('avenir', 12, 'bold'))
    label_file_explorer.grid(column = 0, row = 5)

    #Create styling for buttons and labels
    style = ttk.Style()
    style.configure('TButton', font =
               ('avenir', 12, 'bold'),
                foreground = 'red')
    style.configure('TLabel', font =
               ('avenir', 12, 'bold'),
                foreground = 'white')

    #Create browse files button
    button_explore = ttk.Button(window,
                            text = "Browse Files",
                            style = 'TButton',
                            command = lambda: browseFiles(button_explore, button_quit))
    button_explore.grid(column = 0, row = 8)
    
    #Create quit button
    button_quit = ttk.Button(window,
                    text = "Quit",
                    command = exit)
    button_quit.grid(column = 0,row = 9)


#Adapted from https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
#Used to browse files
def browseFiles(button_explore, button_quit):
    global label_file_explorer
    input_file_name = filedialog.askopenfilename(initialdir = "~/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt"),
                                                       ))
    #Configure label to say pathname
    label_file_explorer.configure(text="File Opened: "+input_file_name)
    label_file_explorer.configure(text="File Opened: "+input_file_name)
    openFile(input_file_name, button_explore, button_quit)

#Function to open and initially process the file
def openFile(input_file_name, button_explore, button_quit):
    #Call global variable
    global label_file_explorer
    #Try to open and import content into input_data
    try:
        input_file = open(input_file_name,'r')
        input_data = input_file.readlines()
        input_file.close()
        #Destroy unneeded button
        button_explore.destroy()
        button_quit.destroy()
        button_quit = ttk.Button(window,
                    text = "Quit",
                    command = exit).grid(column = 0,row = 7,padx = 20, pady = 10)
    #Handle IOError
    except IOError:
        label_file_explorer.configure(text=f"There was an error opening {os.path.basename(input_file_name)}, please try again.")
        #Handle clicking cancel on file selection
        if input_file_name=="":
            label_file_explorer.configure(text=f"File Opened: none")
    #Handle UnicodeDecodeError error
    except UnicodeDecodeError:
        label_file_explorer.configure(text=f"There was an error opening {os.path.basename(input_file_name)}. This program only accepts plaintext .txt files.")
    #Proceed to jobs and skills intake
    else:
        intakeJobsSkills(input_data)

def intakeJobsSkills(input_data):
    #Create dict
    job_skills_dict={}
    
    #Function to take in job names and add them to dict, then request skills and append
    def jobName():
        #Prevent blank job input
        if jobs_input.get()=="":
            label.configure(text= 'You did not input a job. Try again.')
        #Add to dict and configure label, disable input field
        else:
            job_skills_dict[jobs_input.get()]=[]
            #jobs=""+jobs_input.get()
            label.configure(text= string.capwords(jobs_input.get()) + ' added.')
            jobEntered["state"] = DISABLED
            #Function to process skills
            def appendSkill():
                #Prevent blank skills input
                if skills_input.get()=="":
                    label_skills.configure(text= 'You did not input a skill. Try again.')
                #Append skills and configure text field, delete prior contents of field
                else:
                    job_skills_dict[jobs_input.get()].append(skills_input.get())
                    label_skills.configure(text= skills_input.get() + ' added to ' + jobs_input.get() + '.')
                    skillEntered.delete("0", "end")

            #Create skills label
            label_skills = ttk.Label(window, text = f"Enter skill for {jobs_input.get()}:")
            label_skills.grid(column = 0, row = 14)

            #Create skills entry
            skills_input = tk.StringVar()
            skillEntered = ttk.Entry(window, width = 15, textvariable = skills_input)
            skillEntered.grid(column = 0, row = 15)

            #Create add skills button
            skills_button = ttk.Button(window, text="Add Skill", command = appendSkill)
            skills_button.grid(column= 0, row = 16)

            #Function to handle job input finished, delete skills related components and give option to ru analysis
            def stop():
                print(job_skills_dict)
                jobEntered["state"] = NORMAL
                skillEntered["state"] = DISABLED
                label_skills.destroy()
                skillEntered.destroy()
                skills_button.destroy()
                add_next_job_button.destroy()

                jobEntered.delete("0", "end")
                
                #Enter into processing algorithm
                def runAnalysis():
                    comparisonAlgorithm(job_skills_dict, input_data)
                
                #Create run analysis button
                analysis_button = ttk.Button(window, text = "Run Analysis", command = runAnalysis)
                analysis_button.grid(column= 0, row = 18)
            #Create job input finished button
            add_next_job_button = ttk.Button(window, text = "Job Input Finished", command = stop)
            add_next_job_button.grid(column= 0, row = 17)
    
    #Create job label
    label = ttk.Label(window, text = "Enter job needing fulfillment: ")
    label.grid(column = 0, row = 11,padx = 20, pady = 5)
    #Create job input
    jobs_input = tk.StringVar()
    jobEntered = ttk.Entry(window, width = 15, textvariable = jobs_input)
    jobEntered.grid(column = 0, row = 12)
    #Create add job button
    jobs_button = ttk.Button(window, text = "Add Job", command = jobName)
    jobs_button.grid(column= 0, row = 13)

#Function to compare and process workers, jobs, and skills
def comparisonAlgorithm(job_skills_dict, input_data):

    #Create evaluating jobs label
    label_evaluating = ttk.Label(window, text = f'Evaluating jobs...')
    label_evaluating.grid(column = 0, row = 19,padx = 20, pady = 5)

    #Update errored workers list
    def updateErrors(worker_name):
        errors.append(worker_name)


    #Iterate over keys (jobs) inputted by user
    for job in job_skills_dict:
        #Convert to proper formatting for job string
        job_formatted=string.capwords(job)
        #Create dict and list
        job_candidates={}
        errors=[]
        desired_skills=job_skills_dict[job]
        #Iterate over input_data with each person
        for line in input_data:
            #Split at / and , to break down names, skills, and experiences
            line.rstrip('\n')
            list_entry = line.split('/')
            worker_name = list_entry[0].strip()
            score=0
            try:
                #Split at ,
                worker_skills_list = list_entry[1].strip().split(', ')
            #Handle IndexError
            except IndexError:
                updateErrors(worker_name)
                line = line.rstrip('\n')
            else:
                try:
                    past_experience_list = list_entry[2].strip()
                #Handle IndexError
                except IndexError:
                    updateErrors(worker_name)
                    line = line.rstrip('\n')
                #Check if inputted skills in worker skills and add to score if true
                else:
                    for skill in worker_skills_list:
                        if skill in desired_skills:
                            score+=1
                    #Check if inputted job in worker experience and add to score if true
                    if job in past_experience_list:
                        score+=1.5
            job_candidates[worker_name]=score
        #Sortation of workers by score, greatest to least
        sort_orders = sorted(job_candidates.items(), key=lambda x: x[1], reverse=True)
        #Handle exporting of processed data
        f = filedialog.asksaveasfile(mode='a', defaultextension=".txt", initialfile = "output", title=f"Where should {job_formatted.lower()} results be exported?")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        #Enter into function to write data
        writeExport(job_formatted, sort_orders, f)
        label_evaluating.destroy()
        #List printed into console for debugging if user isn't showing up in final results.
        print(errors)
    #Create "finished" label
    label_finished = ttk.Label(window, text = 'The program has successfully executed. You may now press "Quit"')
    label_finished.grid(column = 0, row = 20,padx = 20, pady = 5)

#Export rankings into specified file
def writeExport(job_formatted, sort_orders, f):
    #Write intro line
    f.write(f'\nRanking for {job_formatted} from best to worst match:')
    #Iterate over individuals and write name & score
    for i in sort_orders:
        f.write('\n')
        f.write(f'{i[0]}\t Score: {i[1]}')
    #Insert break line
    f.write('\n')
    #Close file
    f.close()

# Create application window
window = tk.Tk()
#Set window title
window.title("Project Zenith")
#Set minsize for window
window.minsize(993,700)

#Connect interface with window
user_interface(window)

# Start window event loop
window.mainloop()