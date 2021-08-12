import discord
import os
import subprocess
from discord.ext import commands

# Set of whitelisted Discord IDs for strifesnake.
ADMIN_IDs = {"ADMIN_IDs_HERE"}
# Path to dir that will contain user directories.
PATH = "USER_DIR_PATH_HERE"


bot = commands.Bot(command_prefix='$')


# Signals that bot is online.
@bot.event
async def on_ready():
    print("Bot is ready.")


# Handling incorrect commands.
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command. Type $help for list of commands.")


# Detects if a user's unique directory exists.
# If it does not, it attempts to create one.
# Used by all commands.
# Upon exception encounter, exception output is converted to string
# and returned to be output to both console and discord.
# Otherwise, 'True' is returned.
def does_dir_exist_handler(user_dir):
    if not os.path.isdir(user_dir):
        try:
            os.mkdir(user_dir)
        except OSError as e:
            return "OSError encountered when trying to create user dir:\n{}".format(str(e))
        except Exception as e:
            return "Unexpected exception encountered when trying to create user dir:\n{}".format(str(e))
    return True


# Grabs unique Discord ID of requesting user.
@bot.command(pass_context=True)
async def grab_id(ctx):
    await ctx.send(str(ctx.message.author.id))


# Attempts to create a new file for user.
@bot.command(pass_context=True)
async def create(ctx, file_name):
    # Returns if file_name doesn't end in .py or .txt
    if len(file_name) < 4 or (file_name[-3:] != ".py" and file_name[-4:] != ".txt") or file_name.find("/") >= 0:
        await ctx.send("Invalid valid file extension. Must end in .py or .txt")
        return
    # Returns if ID is not whitelisted.
    user_id = str(ctx.message.author.id)
    if user_id not in ADMIN_IDs:
        await ctx.send("You do not have permission to use this bot!")
        return
    # Creates path to user_dir.
    user_dir = PATH + user_id
    # Captures return of does_dir_exist_handler.
    dir_err_msg = does_dir_exist_handler(user_dir)
    # If dir_err_msg == True, then the dir either already existed or was created.
    # If not dir_err_msg, then an exceptions was encountered; prints/sends error string and returns.
    if not dir_err_msg:
        print(dir_err_msg)
        await ctx.send(dir_err_msg)
        return
    # new_file = path to new file.
    new_file = user_dir + "\\" + file_name
    # If it already exists, no need to create a new file. Returns.
    if os.path.exists(new_file):
        await ctx.send("File already exists")
        return
    # Attempts to create new file.
    try:
        open(new_file, "w")
        await ctx.send("File successfully created.")
    except IOError as e:
        io_error_output = f"IOError encountered when attempting to create file:\n{str(e)}"
        print(io_error_output)
        await ctx.send(io_error_output)
    except Exception as e:
        exception_output = f"Unexpected Exception encountered when attempting to create file:\n{str(e)}"
        print(exception_output)
        await ctx.send(exception_output)


# Lists user's directory
@bot.command(pass_context=True)
async def ls(ctx):
    # Returns if ID is not whitelisted.
    user_id = str(ctx.message.author.id)
    if user_id not in ADMIN_IDs:
        await ctx.send("You do not have permission to use this bot!")
        return
    # Creates path to user_dir.
    user_dir = PATH + user_id
    # Captures return of does_dir_exist_handler.
    dir_err_msg = does_dir_exist_handler(user_dir)
    # If dir_err_msg == True, then the dir either already existed or was created.
    # If not dir_err_msg, then an exceptions was encountered; prints/sends error string and returns.
    if not dir_err_msg:
        await ctx.send(dir_err_msg)
        return
    # Attempts to list directory and send to user.
    try:
        output = os.listdir(user_dir)
        await ctx.send("Contents of your directory:")
        await ctx.send(output)
    except OSError as e:
        os_error_output = f"OSError encountered when trying to list dir:\n{str(e)}"
        print(os_error_output)
        await ctx.send(os_error_output)
        return
    except Exception as e:
        exception_output = f"Exception encountered when attempting to list contents of dir.{str(e)}"
        print(exception_output)
        await ctx.send(exception_output)
        return


# Attempts to delete a file.
@bot.command(pass_context=True)
async def delete(ctx, file_name):
    # Returns if ID is not whitelisted.
    user_id = str(ctx.message.author.id)
    if user_id not in ADMIN_IDs:
        await ctx.send("You do not have permission to use this bot!")
        return
    # Creates path to user_dir.
    user_dir = PATH + user_id
    # Captures return of does_dir_exist_handler.
    dir_err_msg = does_dir_exist_handler(user_dir)
    # If dir_err_msg == True, then the dir either already existed or was created.
    # If not dir_err_msg, then an exceptions was encountered; prints/sends error string and returns.
    if not dir_err_msg:
        print(dir_err_msg)
        await ctx.send(dir_err_msg)
        return
    file_to_delete = user_dir + "\\" + file_name
    # Attempt to delete file
    if os.path.exists(file_to_delete):
        try:
            os.remove(file_to_delete)
            await ctx.send("File removed.")
            return
        except OSError as e:
            os_error_output = f"OSError encountered while attempting to delete file:\n{str(e)}"
            print(os_error_output)
            await ctx.send(os_error_output)
            return
        except Exception as e:
            exception_output = f"Exception occurred while attempting to delete file.\n{str(e)}"
            print(exception_output)
            await ctx.send(exception_output)
            return
    await ctx.send("File does not exist.")


# Attempts to read a file's contents
@bot.command(pass_context=True)
async def read(ctx, file_name):
    # Returns if ID is not whitelisted.
    user_id = str(ctx.message.author.id)
    if user_id not in ADMIN_IDs:
        await ctx.send("You do not have permission to use this bot!")
        return
    # Creates path to user_dir.
    user_dir = PATH + user_id
    # Captures return of does_dir_exist_handler.
    dir_err_msg = does_dir_exist_handler(user_dir)
    # If dir_err_msg == True, then the dir either already existed or was created.
    # If not dir_err_msg, then an exceptions was encountered; prints/sends error string and returns.
    if not dir_err_msg:
        await ctx.send(dir_err_msg)
        return
    # Attempts to read file
    file_to_read = user_dir + "\\" + file_name
    if os.path.exists(file_to_read):
        try:
            file_reader = open(file_to_read, "r")
            output_buffer = str(file_reader.read())
            file_reader.close()
            await ctx.send("Contents of {}:".format(file_name))
            await ctx.send(output_buffer)
            return
        except OSError as e:
            os_error_output = f"OSError encountered while attempting to read file:\n{str(e)}"
            print(os_error_output)
            await ctx.send(os_error_output)
            return
        except Exception as e:
            exception_output = f"Exception occurred while attempting to read file.\n{str(e)}"
            print(exception_output)
            await ctx.send(exception_output)
            return
    await ctx.send("File does not exist.")


# Allows user to write to file.
# Captures wanted contents of file in "text"
@bot.command(pass_context=True)
async def write(ctx, file_name, *, text):
    text = str(text)
    user_id = str(ctx.message.author.id)

    # Returns if file_name doesn't end in .py or .txt
    if len(file_name) < 4 or (file_name[-3:] != ".py" and file_name[-4:] != ".txt"):
        await ctx.send("Invalid valid file extension. Must end in .py or .txt")
        return
    # Returns if ID is not whitelisted.
    if user_id not in ADMIN_IDs:
        await ctx.send("You do not have permission to use this bot!")
        return
    # Creates path to user_dir.
    user_dir = PATH + user_id
    # Captures return of does_dir_exist_handler.
    dir_err_msg = does_dir_exist_handler(user_dir)
    # If dir_err_msg == True, then the dir either already existed or was created.
    # If not dir_err_msg, then an exceptions was encountered; prints/sends error string and returns.
    if not dir_err_msg:
        await ctx.send(dir_err_msg)
        return
    # Attempts to write to file
    file_to_write = user_dir + "\\" + file_name
    if os.path.isfile(file_to_write):
        try:
            opened_file = open(file_to_write, "w")
            opened_file.write(text)
            opened_file.close()
            await ctx.send("File written to.")
            return
        except OSError as e:
            os_error_output = f"OSError encountered while attempting to write to file:\n{str(e)}"
            print(os_error_output)
            await ctx.send(os_error_output)
            return
        except Exception as e:
            exception_output = f"Exception occurred while attempting to write to file.\n{str(e)}"
            print(exception_output)
            await ctx.send(exception_output)
            return
    await ctx.send("File does not exist / incorrect file name.")


# Attempts to run .py files
# All of stdout from .py process is sent to a string at end of execution.
# All stdin to be sent to .py process can be sent via *args upon $run command
@bot.command(pass_context=True)
async def run(ctx, file_name, *args):
    # Returns if file isn't .py
    if len(file_name) < 4 or file_name[-3:] != ".py":
        await ctx.send("Invalid valid file extension. Must end in .py")
        return
    # Returns if ID is not whitelisted.
    user_id = str(ctx.message.author.id)
    if user_id not in ADMIN_IDs:
        await ctx.send("You do not have permission to use this bot!")
        return
    # Creates path to user_dir.
    user_dir = PATH + user_id
    # Captures return of does_dir_exist_handler.
    dir_err_msg = does_dir_exist_handler(user_dir)
    # If dir_err_msg == True, then the dir either already existed or was created.
    # If not dir_err_msg, then an exceptions was encountered; prints/sends error string and returns.
    if not dir_err_msg:
        await ctx.send(dir_err_msg)
        return
    # Attempts to run .py script.
    script_to_run = user_dir + "\\" + file_name
    if os.path.exists(script_to_run):
        try:
            # Creates a subprocess via subprocess.Popen
            # stdout and stdin set to subprocess.PIPE
            sub_p = subprocess.Popen(["Python3", "-u", script_to_run], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            # Send each element in *args as individual stdin write.
            for user_input in args:
                user_input = user_input+"\n"
                sub_p.stdin.write(user_input.encode())
            # Once all input is sent, retrieve output and end execution of subprocess.
            output = sub_p.communicate()[0]
            # Sends output of .py script.
            await ctx.send(f"{file_name} output:\n{output.decode()}")
        except subprocess.TimeoutExpired as e:
            timeout_expired_exception_output = f"Timeout expired while waiting for {file_name}:.\n{str(e)}"
            print(timeout_expired_exception_output)
            await ctx.send(timeout_expired_exception_output)
            return
        except subprocess.CalledProcessError as e:
            called_process_error_output = f"{file_name} returned a non-zero exit status:\n{str(e)}"
            print(called_process_error_output)
            await ctx.send(called_process_error_output)
            return
        except Exception as e:
            exception_output = f"Unexpected exception occurred while running {file_name}\n{str(e)}"
            print(exception_output)
            await ctx.send(exception_output)
        finally:
            return
    await ctx.send("File not found.")


bot.run("BOT_TOKEN_HERE")
