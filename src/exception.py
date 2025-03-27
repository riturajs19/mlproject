import sys

def error_message_detail(error, error_detail:sys):
    _,_,exc_tb= error_detail.exc_info() ## This tells where in the file there is an exception
##sys.exc_info() returns information about the exception that was last raised.
##exc_tb stores the traceback object, which contains details about where the error happened.

    file_name =  exc_tb.tb_frame.f_code.co_filename
    #exc_tb.tb_frame.f_code.co_filename retrieves the name of the script where the error was raised.
    error_meassge = "Error occured in python script name[{0}] line number[{1}] error meassage[{2}]".format(
    file_name,exc_tb.tb_lineno,str(error)
#{0} → Filename where the error happened.
#{1} → Line number where the error happened.
#{2} → The actual error message.
)

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail = error_detail)

    def __str__(self):
        return self.error_message
    
## Example- Error occurred in python script [test.py], line number [2], error message [division by zero]
