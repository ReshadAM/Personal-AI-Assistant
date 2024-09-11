# Standard library imports
import csv
import json
import os
import re
import sys

# Third-party imports
from icecream import ic
from rich.console import Console
from rich.panel import Panel
import simpleaudio as audioPlayer

# My API helper Class imports 
from GPT import MyAI
from elevenAPI import ElevenAPI
from speech_to_text import speech_to_text_converter




def print_boxed_message(message, border_color="white"):
    """
    Displays a message within a styled box to make the UI more user friendly

    Parameters:
        message (str): The message to be displayed.
        border_color (str): The color of the border around the message box. (Default=White)
    """
    console = Console()
    console.print(Panel(message, border_style=border_color, expand=False))


def update_shopping_list(items: dict) -> bool:
    """
    Update the shopping list CSV file with new items with their respecetive quantities 
    or updates quantities if items already exist.

    Parameters:
        items (dict): A dictionary where keys are item names and values are their quantities.

    Returns:
        bool: True if the update was successful, False if an error occurred.
    """ 
    try:
        # Check if the file shopping_lists.csv has been created yet
        file_exists = os.path.isfile("shopping_list.csv")

        # Read the existing items from the CSV file and assign them to a dictionary
        existing_items = {}
        if file_exists:
            try:
                # Read the CSV file and assign all the items and their quantities to a dictionary
                with open('shopping_list.csv', mode='r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        existing_items[row['Item'].lower()] = int(row['Quantity'])
            except csv.Error as e:
                print(f"There was an error trying to read the CSV file: {e}")
                return False

        # Update the quantities for items that already exist
        for item in items['items']:
            item_name = item['item'].lower()
            quantity = int(item['quantity'])

            # Update the quantity if the item already exists
            if item_name in existing_items:
                existing_items[item_name] += quantity
            else:
                # If the item does not exist, then add it to the dictionary with its assigned quantity
                existing_items[item_name] = quantity

        # Override the CSV file with the updated shopping list data stored in existing_items
        try:
            with open('shopping_list.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Item', 'Quantity'])
                for item_name, quantity in existing_items.items():
                    writer.writerow([item_name, quantity])

            return True
        except csv.Error as e:
            print(f"There was an error trying to write into the CSV file: {e}")
            return False

    except Exception as ee:
        print(f"Some error occurred: {ee}")
        return False


def create_file(fileName: str) -> bool:
    """
    Creates a new file with the specified name in the 'created_files' directory.
    If the file already exists, prompts the user for confirmation before overriding it

    Parameters:
        fileName (str): The name of the file to be created.

    Returns:
        bool: True if the file was created or overwritten successfully, False if the operation was canceled or some error occurred.
    """
    # Make the directory if it does not already exist
    directory = "created_files"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Construct the path for the file
    file_path = os.path.join(directory, fileName)

    file_exists = os.path.isfile(file_path)

    if file_exists:
        print_boxed_message("A file with that name already exists, are you sure you want to override it? (Y\\N)", border_color="red")
        ElevenAPI().generate_voice("A file with that name already exists, are you sure you want to override it? (Yes\\No)")
        user_choice = input("(Y\\N):")

        while True:
            if user_choice.upper() == "Y" or user_choice.upper() == "YES":
                with open(file_path, "w") as file:
                    pass
                return True
            elif user_choice.upper() == "N" or user_choice.upper() == "NO":
                break
            else:
                print("Wrong input")
                user_choice = input("(Y\\N):")
    else:
        with open(file_path, "w") as file:
            pass
        return True

    return False


def endChat()->None:
    """
   endChat is used to end the program. It generates a goodbye messege and shuts the system. using sys.exit.
  
    Parameters:
        None

    Returns:
        None
    """

    print_boxed_message("Goodbye! Have a great day!", border_color="cyan")
    ElevenAPI().generate_voice("Goodbye! Have a great day!")
    sys.exit(1)

def add_data_to_file(fileName: str, data: str) -> bool:
    """
    Adds data to existing files, or if the file does not exist it will prompted
    the user, then create the file and then add the requested data to it.
    Supports adding data to (.txt) files and adding new rows to (.csv) files.
  
    Parameters:
        fileName (str): The name of the file to which data will be added.
        data (str): The data to be added to the file.

    Returns:
        bool: True if the data was successfully added, False if the operation 
        was canceled or an error occurred.
    """
    # Make the directory if it does not already exist
    directory = "created_files"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Construct the path for the file
    file_path = os.path.join(directory, fileName)

    file_exists = os.path.isfile(file_path)

    if file_exists:
        _, file_extension = fileName.split(".")

        # If the file is a txt file, then simply add the data to it.
        if file_extension == 'txt':
            # Adding data to the txt file
            with open(file_path, 'a') as file:
                file.write(data + '\n')
            return True
        elif file_extension == 'csv':
            # Read and save the current contents of the file
            with open(file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                rows = list(reader)

            # Append the data to a new row
            rows.append([data])

            # If the file is a csv file, then use the csv library to add to the next row in the file
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            return True
        else:
            # For now the program will only add to txt, and csv files
            print_boxed_message(f"Sorry, adding to files of type {file_extension} is currently unavailable")
            ElevenAPI().generate_voice(f"Sorry, adding to files of type {file_extension} is currently unavailable")
            return False
    else:
        print(f'The file {fileName} does not exist, would you like to create the file? (Y\\N)')
        ElevenAPI().generate_voice(f'The file {fileName} does not exist, would you like to create the file? (Yes\\No)')
        user_choice = input("(Y\\N):")
        while True:
            if user_choice.upper() == "Y" or user_choice.upper() == "YES":
                with open(file_path, "w") as file:
                    pass
                return add_data_to_file(fileName=fileName, data=data)
            elif user_choice.upper() == "N" or user_choice.upper() == "NO":
                break
            else:
                print("Wrong input")
                user_choice = input("(Y\\N):")
    return False

def check_special_command(prompt: str) -> str:
    """
    This function is responsible for checking the provided OPEN AI prompt for special commands
    related to shopping lists, file creation, or data appending. Executes the appropriate action based on 
    the detected command.

    The OPEN AI model is responsible for ensuring the correct output is produced to complete the special
    tasks, like adding data to a shoping list.

    Parameters:
        prompt (str): The prompt string containing the potential special command.

    Returns:
        str: A message indicating the result of the command execution or None 
        if no valid command was found. This mean eather the OPEN AI failed to produce the correct
        output, or the user requested something that not fall under the special command. 
    """
    # Using regular expression to ensure the OpenAI response is in the expected format
    command1 = re.search(r'\b(ADD|DELETE)\|({.*?})\s*\|\s*(.*)', prompt)  # Shopping list adding and deleting
    command2 = re.search(r'\b(CREATE)\s*\|\s*\"(\s*.*\..*\s*)\"\s*\|\s*(.*)', prompt)  # Creating files
    command3 = re.search(r'\b(APPEND)\s*\|\s*\"(.*\..*)\"\s*\|\s*.*\{(.*)\}\s*.*\"(.*)\".*', prompt)  # Adding data to files

    try:
        # shoping list adding/deleting
        if command1:
            action = command1.group(1)
            data = command1.group(2)
            ai_messege = command1.group(3)

            if action == 'ADD':
                items_dict = json.loads(data)
                add_request = update_shopping_list(items_dict)

                if add_request:
                    return ai_messege
                else:
                    fail_messege = ai_messege.split("Added")
                    return f"Sorry, something went wrong, I was not able to add: {fail_messege}"

            elif action == "DELETE":
                return "The delete feature is currently unavailable"

            else:
                return "I cannot do that right now"
        # File creation 
        elif command2:
            action = command2.group(1)
            data = command2.group(2)
            ai_messege = command2.group(3)

            if action == "CREATE":
                created_file = create_file(data)

                if created_file:
                    return ai_messege
                else:
                    return f'Failed to create the file {data}'

            else:
                return "I cannot do that task right now"

        # Adding data to files
        elif command3:
            action = command3.group(1)
            filename = command3.group(2)
            data = command3.group(3)

            if action == "APPEND":
                if filename != command3.group(4):
                    return "There was some sort of error, please rephrase the request"
                else:
                    if add_data_to_file(fileName=filename, data=data):
                        return f'Added {data} to the file {filename}'
                    return f"Failed to add data to the {filename} as it does not exist"
            else:
                return "I cannot do that at the moment"
        # Secret Phrase's
        else:
            secret_command = re.search(r'^SECRET_PHRASE_USED:ORDER\((.*)\)$', prompt)
            if secret_command:
                # Secret command 687 means put the computer to sleep
                if secret_command.group(1) == '687':
                    if put_computer_to_sleep(secret_command.group(1)):
                        ElevenAPI().generate_voice("It's done")
                        return "687"
                # secret command 625 means the user wants to end the chat
                elif secret_command.group(1) == '625':
                     # Call the endChat() function, to end the chat
                    endChat()
                    return '625'
                else:    
                    return None
            else:
                return None

    except Exception as e:
        print(f"There was some sort of error executing your request {e}")
        return f"There was some sort of error executing your request.\nError type: {e}"


def starting_choice() -> str:
    """
    Presents an introductory message to the user, explaining the Rachels's capabilities.
    Then prompts the user to choose their input method: text or speech.

    Returns:
        str: The user's input preference, where '0' indicates text input and '1' indicates speech input.
    """
    print_boxed_message(
        "Hello! I'm June, your personal AI assistant. I'm here to help with all your questions and to complete a variety of specialized tasks. Here's what I can do:\n\n" +
        "- Add items to your shopping list\n" +
        "- Create new files\n" +
        "- Delete existing files\n" +
        "- Add data to specific files\n\n" +
        "Feel free to ask me anything, or just let me know what task you'd like me to handle. Type 'exit', 'bye', or 'done' to end our chat.",
        border_color="cyan"
        )

    # To save on resources, the starting messege will be played using a wav file. 
    if os.path.exists('audio_files/June_greetings_message.wav'):
        sound_obj = audioPlayer.WaveObject.from_wave_file('audio_files/June_greetings_message.wav')
        play_sound_obj = sound_obj.play()
        play_sound_obj.wait_done()
    else:
        # If the audio file does not eixst, then simply generate the audio using the Eleven Labs API
        ElevenAPI().generate_voice(
       "Hello! I'm June, your personal AI assistant. I'm here to help with all your questions and to complete a variety of specialized tasks. Here's what I can do:\n\n" +
        "- Add items to your shopping list\n" +
        "- Create new files\n" +
        "- Delete existing files\n" +
        "- Add data to specific files\n\n" +
        "- Put your device to sleep, or answer any of your questions.\n\n" +
        "Feel free to ask me anything, or just let me know what task you'd like me to handle. Type 'exit', 'bye', or 'done' to end our chat."
        )

    user_input_preference = input("Would you like to type your input or use speech? (0 = Text, 1 = Speech): ").strip()

    while user_input_preference not in ["0", "1"]:
        user_input_preference = input("Invalid choice. Please choose 0 for text or 1 for speech: ").strip()

    return user_input_preference


def put_computer_to_sleep(order: str)->bool:
    """
    This function will put the computer to sleep if the correct number is provided. 
    The number system is a way to distinguish future orders when more is added. The goal
    behind this is to show that the AI can capture certin comands that allow the user to pre-program certin
    actions, like putting a computer to sleep. 

    Parameters:
        order (str): A 3 digit string, that will ensure the correct order was given and the correct function was called. 
    Returns:
        bool: a bool value that indicates weather the function completed its task or not.
    """
    if order == "687":
        user = "Y"
        if user.upper() == "Y" or user.upper() == "Yes":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return True
        else:
            print("Failed")
    else:
        print("Wrong order code was given:", order)
        return False
        


def main():
    try:
        # Initializing objects
        ai_client = MyAI()
        voice_client = ElevenAPI()

        user_input_preference = starting_choice()

        while True:

            # If the user want to use manual input 
            if user_input_preference == "0":
                user_input = input("You: ")
                print_boxed_message(f"You: {user_input}", border_color="green")
            else:
                # Use Google's text to speech API to convert voice to text 
                # If the user choose's to use verbal input
                print("Listening...")
                client = speech_to_text_converter()
                user_input = client.record_text()
                print_boxed_message(f"You: {user_input}", border_color="green")

            # Check for exit commands
            if user_input.lower().strip() in ["exit", "bye", "done"]:
                print_boxed_message("Goodbye! Have a great day!", border_color="cyan")
                voice_client.generate_voice("Goodbye! Have a great day!")
                break
            else:
                print("Processing with GPT-4o...")
                response_text = ai_client.chat_with_gpt(user_input)

                # Parsing special commands if found
                special_command_response = check_special_command(response_text)

                # Check if the user asked for one of the special commands, like adding elements to a shopping list
                if special_command_response is not None:
                    
                    print_boxed_message(f'AI: {special_command_response}', border_color="red")
                    voice_client.generate_voice(special_command_response)

                else:
                    print_boxed_message(f"AI: {response_text}", border_color="red")
                    voice_client.generate_voice(response_text)

    except KeyboardInterrupt:
        print("\n[HELP] Forced Shutdown")


if __name__ == "__main__":
    main()
