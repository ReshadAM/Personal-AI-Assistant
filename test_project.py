from project import create_file,add_data_to_file,update_shopping_list
from unittest.mock import patch, mock_open
import pytest
import os




'''

This function will test the create_file() function in the project file. Due to the confines of the 
CS50 final project, all the tests for the spesefic project function must be done in a single test function. 

'''


def test_create_file():
    # Create the directory if it does not exist, if it does, do nothing 
    os.makedirs('created_files',exist_ok=True)

    # Test case 1: Test for createing a text file

    fileName = 'testFile.txt'
    filePath = os.path.join('created_files/',fileName)

    assert create_file(fileName) == True # check if the function returns True 
    assert os.path.exists(filePath) == True # check if the file was created
    os.remove(filePath) # remove the testfile after test

    # Test case 2: Test for createing a CSV file (none-txt file)
    fileName = 'testFile.csv'
    filePath = os.path.join('created_files/',fileName)

    assert create_file(fileName) == True
    assert os.path.exists(filePath) == True
    os.remove(filePath) # remove the testfile after test

    # Test case 3: Test for createing a file with no extension
    fileName = 'testFile'
    filePath = os.path.join('created_files/',fileName)

    assert create_file(fileName) == True
    assert os.path.exists(filePath) == True

    os.remove(filePath)

    # Test case 4: Simulating the user not choosing to overwrite the file 

    fileName = 'testFile.txt'
    filePath = os.path.join('created_files/',fileName)

    with open(filePath,'w') as w:
        w.write('Testing 123')
        
    with patch('builtins.input',return_value = 'N'): # using patch to simulate the user inputting N for no override
        assert create_file(fileName) == False # This should be false as the user choose not to override
    
    # check to ensure the content of the file was not changed 

    with open(filePath, 'r') as r:
        content = r.read()
        assert content == 'Testing 123'

    # remove the file if it was created during the test
    os.remove(filePath)



def test_add_data_to_file():
    directory = 'created_files'
    os.makedirs(directory, exist_ok=True)

     # Test case 1: Add data to an existing text file
    fileName = 'testFile.txt'
    filePath = os.path.join(directory, fileName)
    data = "Test data"
    create_file(fileName)

    # Checking if the function returns true as an indication that data was added to the file 
    assert add_data_to_file(fileName, data) == True 

    # Check if the function added data correctly
    with open(filePath, 'r') as file:
        contents = file.read()
    assert contents == data + "\n"
    os.remove(filePath)  # Remove the file after the test

    # Test case 2: Add data to an existing CSV file
    fileName = 'testFile.csv'
    filePath = os.path.join(directory, fileName)
    create_file(fileName) 
    data = "Test Data"

    # Checking if the function returns true as an indication that data was added to the file 
    assert add_data_to_file(fileName, data) == True

    # Check if the function added data correctly
    with open(filePath, 'r') as file:
        contents = file.read()
    assert contents == data + "\n"
    os.remove(filePath)  # Remove the file after the test


    # Test case 3: Try to add data to a non-existent file and choose to create it
    fileName = 'newFile.txt'
    filePath = os.path.join(directory, fileName)
    data = "Test Data"
    # Simulate user choosing to create the file by inputting Y for yes
    with patch('builtins.input', return_value='Y'): 
         # Check if the function returns True
        assert add_data_to_file(fileName, data) == True 

    # check if the function correctly added the new file and data
    with open(filePath, 'r') as file:
        contents = file.read()
    assert contents == data + "\n"
    os.remove(filePath)  # Remove the file after the test

    # Test case 4: Try to add data to a non-existent file and choose not to create it
    fileName = 'newFile.csv'
    filePath = os.path.join(directory, fileName)
    data = "Test data"
    # Simulate user choosing not to create the file by inputting N for no
    with patch('builtins.input', return_value='N'):  
        assert add_data_to_file(fileName, data) == False  

    # check to make sure the file was not created
    assert not os.path.exists(filePath)



def test_update_shopping_list():
    fileName = 'shopping_list.csv'
    filePath = os.path.join(fileName)

    # set the file up, if it already exists, then override it with the starting row
    with open(filePath, 'w') as file:
        file.write("Item,Quantity\n")

    # Test case 1: Update shopping list with a new item
    initial_data = {
        "items": [
            {"item": "milk", "quantity": 3}
        ]
    }
    assert update_shopping_list(initial_data) == True

    # Check to make sure the item was added corrctly
    with open(filePath, 'r') as file:
        contents = file.read()
    assert "milk" in contents
    assert "3" in contents

    # Test case 2: Update shopping list with an existing item. 
    # This test should update the quantity
    update_data = {
        "items": [
            {"item": "milk", "quantity": 3}
        ]
    }
    assert update_shopping_list(update_data) == True

    # Check if the item quantity was updated correctly
    with open(filePath, 'r') as file:
        contents = file.read()
    assert "milk" in contents
    # inital 3 milk's plus the new 3 milk bags.
    assert "6" in contents  

    # Test case 3: Add a different item to the shopping list
    new_item_data = {
        "items": [
            {"item": "banana", "quantity": 2}
        ]
    }
    assert update_shopping_list(new_item_data) == True

    # Check if the new item was added correctly without overrriding the inital one
    with open(filePath, 'r') as file:
        contents = file.read()
    assert "milk" in contents
    assert "6" in contents
    assert "banana" in contents
    assert "2" in contents

    # Cleanup
    os.remove(filePath)
def main():
    pass

if __name__ == '__main__':
    main()