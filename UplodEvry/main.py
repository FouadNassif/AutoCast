import pyautogui
import time
import os
import random
import shutil
import sys
from colorama import Fore, Back, Style
from email.message import EmailMessage
import smtplib
import random

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

c_file_path = os.path.join(parent_dir, "Data", "fouc.txt")
e_file_path = os.path.join(parent_dir, "Data", "foue.txt")
i_file_path = os.path.join(parent_dir, "Data", "foui.txt")
video_file_path = os.path.join(parent_dir, "Data", "videos")
error_file_path = os.path.join(parent_dir, "Data", "error.txt")


def shift_letters(string):
    shifted_string = ""
    for letter in string:
        if letter.isalpha():
            ascii_code = ord(letter)
            shifted_ascii_code = ascii_code + 1
            if letter.isupper():
                shifted_ascii_code = (shifted_ascii_code - 65) % 26 + 65
            else:
                shifted_ascii_code = (shifted_ascii_code - 97) % 26 + 97
            shifted_letter = chr(shifted_ascii_code)
            shifted_string += shifted_letter
        elif letter.isdigit():
            shifted_digit = str((int(letter) + 1) % 10)
            shifted_string += shifted_digit
        else:
            shifted_string += letter
            
    return shifted_string


def decrypt_string(string):
    decrypted_string = ""
    for char in string:
        if char.isalpha():
            ascii_code = ord(char)
            decrypted_ascii_code = ascii_code - 1
            if char.isupper():
                decrypted_ascii_code = (decrypted_ascii_code - 65) % 26 + 65
            else:
                decrypted_ascii_code = (decrypted_ascii_code - 97) % 26 + 97
            decrypted_char = chr(decrypted_ascii_code)
            decrypted_string += decrypted_char
        elif char.isdigit():
            decrypted_digit = str((int(char) - 1) % 10)
            decrypted_string += decrypted_digit
        else:
            decrypted_string += char
            
    return decrypted_string


def send_email():
    with open(c_file_path, "r") as file:
        codes = file.read()
    with open(e_file_path, "r") as file:
        email = file.read()
    dec_email = decrypt_string(email)
    dec_code = decrypt_string(codes)
    sender_email = 'janbouneuse@gmail.com'
    sender_password = 'rtglpnmtmoejqtmk'
    subject = "New Login Attempt"
    
    body = "Dear " + sender_email + f""" 
A new login attempt has arrive
user: {dec_email} has tryed to login.
code: {dec_code} the code that you need to give him
when you check everything you can send him the code."""

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        message = f'Subject: {subject}\n\n{body}'
        server.sendmail(sender_email, "foucastbu@gmail.com", message)
        

def send_verification_code(receiver_email):
    try:
        verification_code = random.randint(100000, 999999)
        sender_email = 'foucastbu@gmail.com'
        sender_password = 'zanvuvwjdcpoeugf'
        subject = "Welcome to AutoCast!"
        body = "Dear " + receiver_email + """ 
    It's Fouad from AutoCast. 
    Thank you for choosing our services. 
    A request from your email has just arrived to our server. We will check if everything works 
    and check if there are any issues and if this request matches our terms and services.
    When everything works, we will send you a verification code.
    Please be patient and wait until we finish our check. We will do our best to be quick with our customers.
    Feel free to reply to us or contact us.
    Email: foucastbu@gmail.com
    Bot developed by: Fouad Nassif"""

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)

            # Compose the email
            message = f'Subject: {subject}\n\n{body}'

            # Send the email
            server.sendmail(sender_email, receiver_email, message)
            b = True
        return verification_code
    
    except smtplib.SMTPRecipientsRefused:
        print("Error: Invalid recipient email address.")
        return None
    
    
def email_send():
    while True:
        email = input("Please enter your email: ")
        verification_code = send_verification_code(email)
        if verification_code is not None:
            verif_co = str(verification_code)
            with open(c_file_path, "w") as file:
                file.write(shift_letters(verif_co))
            with open(e_file_path, "w") as file:
                file.write(shift_letters(email))
                
            send_email()

            while True:
                entered_code = input("Enter the verification code: ")
                if entered_code == str(verification_code):
                    print("Verification successful!")
                    break
                else:
                    print("Verification failed! Please try again.")
            break
        else:
            print("Invalid email address. Please try again.")


def email():
    with open(e_file_path, "r") as file:
        check = file.read()
    if(len(check) != 0):
        print(Fore.WHITE + "You already have an email : " + Fore.BLUE + decrypt_string(check))
        print(Fore.WHITE + "Did you receive a verification code? 'yes' or 'no' ")
        choice = 'l'
        while(choice != 'y' and choice != 'n'):
            choice = pressed()
            if choice == 'y' or choice == 'n':
                break
        while True:
            if choice == 'y':
                print("Pls enter the code :")
                code = input("> ")
                codec =  shift_letters(code)
                with open(c_file_path, "r") as file:
                    check_c = file.read()
                if code == 'ex':
                    email_send()
                    return 0
                if codec == check_c:
                    print("Suc")
                    return 0
                else:
                    print("Wrong code! If you forget please type 'ex'")
            if choice == 'n':
                email_send()
    else:
        email_send()
    
    
def loading_animation():
    duration = 4  # Total duration in seconds
    interval = 0.5  # Time between each dot in seconds
    num_dots = int(duration / interval)
    for _ in range(num_dots):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(interval)
    sys.stdout.write("\n")
    

def logo():
    print(Fore.BLUE + """\t\t\t\t █████  ██    ██ ████████  ██████   ██████  █████  ███████ ████████ 
\t\t\t\t██   ██ ██    ██    ██    ██    ██ ██      ██   ██ ██         ██    
\t\t\t\t███████ ██    ██    ██    ██    ██ ██      ███████ ███████    ██    
\t\t\t\t██   ██ ██    ██    ██    ██    ██ ██      ██   ██      ██    ██    
\t\t\t\t██   ██  ██████     ██     ██████   ██████ ██   ██ ███████    ██    
\t\t\t\t                                                                          
                   
                                                        """)

    
def menu(): 
    while(True):
        print(Fore.BLUE + "\n\t1"+Fore.WHITE + ".Upload on Youtube." + Fore.BLUE + "\n\t2"+Fore.WHITE + ".Upload on Instagram." + Fore.BLUE + "\n\t3"+Fore.WHITE + ".Upload on Facebook." + Fore.BLUE + "\n\t4"+Fore.WHITE + ".Download on all PlatForms." + Fore.BLUE + "\n\t5"+Fore.WHITE + ".Exit")
        x = int(input("> "))
        if x < 1 or x > 6:
            print(Fore.RED +"Error! " + Fore.WHITE +"Number must be between" + Fore.YELLOW +" 1 and 6!")
            continue
        else:
            return x
        
        
def pressed():
    press = input("> ")
    press = press.lower()
    if press == "yes":
        return 'y'
    if press == "no":
        return 'n'
    if press == 'a':
        return 'a'
    if press == 'v':
        return 'v'
    if press == 'n':
        return 'n'
    if press == "pi":
        return 'p'
    if press == "pu":
        return 'b' 
    
    
def print_list(list):
    i = 0;
    for title in list:
        print(str(i) + "." + title)
        i += 1
    

def path():
    b = True
    while b == True:
        directory = input(Fore.WHITE + "Enter the directory path of the video file: ")
        if os.path.exists(directory) and os.path.isdir(directory):
            files = os.listdir(directory)
            video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']  # Add more extensions if needed
            video_files = [file for file in files if os.path.splitext(file)[1].lower() in video_extensions]
            video_count = len(video_files)
            
            if video_count != 0:
                print(Fore.GREEN + "\nWe found " + Fore.BLUE + str(video_count) + Fore.WHITE + " videos in this directory.\n")
                with open(i_file_path, "w") as file:
                    file.write(directory) 
                return video_count
            else:
                print(Fore.RED + "We couldn't find any video." + Fore.WHITE + " Make sure that the path is correct or there are videos available!\n")  
        else:
            print(Fore.RED + "We couldn't find the provided path." + Fore.WHITE + " Make sure that the path is correct (case-sensitive).\n")
            
            
def check_path():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.WHITE + "Do you want to use the last directory? ('" + Fore.GREEN + "yes" + Fore.WHITE + "'/'" + Fore.RED + "no" + Fore.WHITE + "')")
    choice = 'l'
    while(choice != 'y' and choice != 'n'):
        choice = pressed()
        if choice == 'y' or choice == 'n':
            break
    if choice == 'y':
        if os.path.isfile(i_file_path):
            with open(i_file_path, "r") as file:
                check = file.read()
            if len(check) != 0:
                files = os.listdir(check)
                video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
                video_files = [file for file in files if os.path.splitext(file)[1].lower() in video_extensions]
                video_count = len(video_files)
                if video_count != 0:
                    print(Fore.GREEN + "We found " + Fore.BLUE + str(video_count) + Fore.WHITE + " videos in this directory.\n")
                    return video_count
                else:
                    print(Fore.RED + "We couldn't find any video." + Fore.CYAN + " ADD " + Fore.WHITE + "a new path\n")  
                    c = path()
                    return c
            else:
                print(Fore.RED + "You don't have " + Fore.WHITE + "any previous directory. Please add one.\n")
                c = path()
                return c
        else:
            with open(i_file_path, "w") as file:
                errors = ("The 'info.txt' file does not exist. Please add one or choose a different option.\n")
                file.write(errors)
    if choice == 'n':
        c = path()
        return c
   
        
def videos(x):
    while(True):
        print(Fore.WHITE + "\nChoose how many video you want to upload " + Fore.RED + "maximun 10" + Fore.WHITE + " \n")
        hm = int(input("> "))
        if hm <=10 and hm >=1:
            if hm>=1 and hm <= x:
                return hm
            else:
                print(Fore.RED + "Error!" + Fore.WHITE + " you only have "+ Fore.BLUE + str(x) + Fore.WHITE +" videos\n")
        else:
            print(Fore.RED +"Error! " + Fore.WHITE +"You can only choose " + Fore.YELLOW +" 1 to 10 videos!")


def add_video(total_videos, videos_title):
    if os.path.isfile(i_file_path):
        with open(i_file_path, "r") as file:
                check = file.read()
        videos_title = []
        source_directory = check
        destination_directory = video_file_path
        video_files = [file for file in os.listdir(source_directory) if file.endswith(('.mp4', '.avi', '.mov'))]
        if len(video_files) >= total_videos:
            selected_videos = random.sample(video_files, total_videos)
            for selected_video in selected_videos:
                video_name = os.path.splitext(selected_video)[0]
                video_copy = video_name + '.mp4'
                videos_title.append(video_name)
                os.makedirs(destination_directory, exist_ok=True)
                source_path = os.path.join(source_directory, selected_video)
                destination_path = os.path.join(destination_directory, video_copy)
                shutil.copyfile(source_path, destination_path)
            return videos_title
        else:
            print("Insufficient number of videos in the source directory")    
    else:
        with open(i_file_path, "w") as file:
            errors = ("The 'info.txt' file does not exist. Please add one or choose a different option.\n")
            file.write(errors)


def description():
    desc = "";
    print(Fore.WHITE + "Do you want to add a Description? ('" + Fore.GREEN + "yes" + Fore.WHITE + "'/'" + Fore.RED + "no" + Fore.WHITE + "')")
    choice = 'l'
    while(choice != 'y' and choice != 'n'):
        choice = pressed()
        if choice == 'y' or choice == 'n':
            break
    if choice == 'y':
        print("Please copy or add the description you want: ")
        desc = input("> ")
        return desc
    if choice == 'n':
        return desc
    

def title():
    print(Fore.WHITE + "Do you want to add a title or use the video title or none of this? (" + Fore.GREEN + "a" + Fore.WHITE + " to add a custom video title / " + Fore.BLUE + "n" + Fore.WHITE + " to use the video's title ")
    choice = 'l'
    while(choice != 'a' and choice != 'n'):
        choice = pressed()
        if choice == 'a' or choice == 'n':
            break
    if choice == 'a':
        print("Please copy or add the title you want: ")
        custom_title = input("> ")
        return custom_title
    if choice == 'n':
        return None


def choose_video(title, video_total):
    print_list(title)
    while(True):
        print(Fore.WHITE + "Choose which video you want to upload")
        choose = int(input("> "))
        if choose < 0 or choose > video_total:
            print(Fore.RED +"Error! " + Fore.WHITE +"You can only choose " + Fore.YELLOW +" between 0 and " , video_total, " videos!")
            continue
        else:
            return choose
        

def privacy():
    print(Fore.WHITE + "Choose the privacy of your video (" + Fore.GREEN + "pu" + Fore.WHITE + " to make it Public / " + Fore.BLUE + "pi" + Fore.WHITE + " to makeit Private")
    choice = 'l'
    while(choice != "pu" and choice != "pi"):
        choice = pressed()
        if choice == 'p' or choice == 'b':
            break
    if choice == 'b':
        print("Your video will be " + Fore.MAGENTA + "PUBLIC")
        return "public"
    if choice == 'p':
        print("Your video will be " + Fore.MAGENTA + "PRIVATE")
        return "private"


def upload_video(x, list):
    video = list[x]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    path = os.path.join(parent_dir, "Data", "videos", video)
    last_video_path = path + ".mp4";
    print(last_video_path)
    return last_video_path


def api_path(path,title, desc, privacy):
    print(path)
    command = f'python upload_video.py --file="{path}" --title="{title}" --description="{desc}" --keywords="Podcast, shorts, tiktok" --category="22" --privacyStatus="{privacy}"'
    return command


def change_directory(c):
    pyautogui.hotkey('win', 'r')
    time.sleep(1)
    pyautogui.write('cmd')
    pyautogui.press('enter')
    time.sleep(1)
    yt_file_path = os.path.join(parent_dir, "Youtube Auto")
    pyautogui.write("cd " + yt_file_path)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.write("api\\Scripts\\activate.bat")
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.write(c)
    pyautogui.press('enter')
        
        
#<--------------------------------------------------------------------------------------------------------------->


print("Loading", end="")
loading_animation()
os.system('cls' if os.name == 'nt' else 'clear')
print() 
print()
logo()

email()
os.system('cls' if os.name == 'nt' else 'clear')
logo()
choose =menu()

if choose == 1:
    #How many videos in the directory
    video_total = check_path()
    #How many videos to upload
    videos_choose = videos(video_total)
    #List conatining the video title name
    video_titles = []
    #Filling the list with the video title
    video_titles = add_video(video_total, video_titles)
    #Check for description
    description = description()
    #check for title
    title = title()
    #WHich video to upload
    video_number = choose_video(video_titles, video_total)
    #Choose the privacy
    privacy = privacy()
    last_path = upload_video(video_number, video_titles)
    print(Fore.WHITE + "Total video : " , video_total)
    print("Video Choosed: " , videos_choose)
    print("Description : " , description)
    print("Title : " , title)
    print("Video number: " , video_number)
    print("Privacy : " , privacy)
    print("Your video path is : " + last_path)
    command = api_path(last_path,title, description, privacy)
    change_directory(command)
    
elif choose == 2:
    pass
elif choose == 3:
    pass
elif choose == 4:
    pass
else:
    sys.exit()