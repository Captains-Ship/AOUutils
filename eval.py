import traceback
import os
import sys
while True:
    try:
        inputted = input('>>> ')
        eval(inputted)
    except Exception as error:
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
