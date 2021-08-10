# Strife-Snake
Python-based Discord bot that allows users to manage their own personal directory and create/run their own pythons scripts, all within Discord.

Utilizes the Discord.py libraries to guide the interactions between Discord user and Strife Snake.
Automatically creates personal dir for Discord user based on their Discord ID

## Example Usecase
![Strife-Snake screenshot](StrifeSnake_UseCase.PNG)

## Command List

Create: Allows user to create .py or .txt files.
  
  $create <file>
  
Delete: Allows user to delete .py or .txt files.
  
  #delete <file>

Grab_ID: Prints out sender's Discord ID
  
  $grab_id

Help: Displayes list of commands.
  
  $help <command>
  
List: Lists contests of personal dir.
  
  $ls
  
Read: Displayes contents of a file to user.
  
  $read <file>
  
Run: Allows user to run .py file. Outputs stdout to user. Stdin is taken in as args during command.
  
  $run <file> [input arguments]
  
Write: Allows user to write to a .txt or .py file.
  
  $write <file> 
  [File Contents]
