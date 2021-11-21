#Tomek Botwicz
#CS21
#Project Zenith

import time

def main():

    print('-'*150,'''\nHello and welcome to Project Zenith, an intelligent economic decision-making tool!
    Inspired by Project Cybersyn, it can recommend worker allocation to open posts based on personal skills and past job experience.
    To begin, please enter the filename to be imported. Each line should be formatted as such: NAME / SKILLS (COMMA SEPARATED) / PAST JOBS (COMMA SEPARATED)\n''','-'*150)

    successfully_opened = False

    while successfully_opened == False:
        input_file_name = input('Input File (enter Q to exit): ')
        if input_file_name != 'Q' and input_file_name != 'q':
            try:
                input_file = open(input_file_name,'r')
            except FileNotFoundError:
                print('That file could not be found. Please try again.')
            except IOError:
                print('That file could not be read. Please try again.')
            else:
                technician_skills = ['technical', 'creative']
                human_resources_skills = ['charismatic', 'creative']
                sales_skills = ['analytical', 'integrative']
                successfully_opened = True
                imported_worker = input_file.readline()
                imported_worker = imported_worker.rstrip('\n')
                while imported_worker != "":
                    list_entry = imported_worker.split('/')
                    list_entry[0] = list_entry[0].strip()
                    skills_list = list_entry[1].split(',')
                    technician_check = [skill for skill in technician_skills if(skill in list_entry[1])]
                    human_resources_check = [skill for skill in human_resources_skills if(skill in list_entry[1])]
                    sales_check = [skill for skill in sales_skills if(skill in list_entry[1])]
                    print(f'Processing {list_entry[0]}...')
                    time.sleep(2)
                    print(list_entry)
                    print(skills_list)
                    print(str(bool(technician_check)))
                    print(str(bool(human_resources_check)))
                    print(str(bool(sales_check)))

                    imported_worker = input_file.readline()
                    imported_worker = imported_worker.rstrip('\n')
                input_file.close()
        else:
            successfully_opened = True
            print('Successfully terminated program. See you next time!')

main()