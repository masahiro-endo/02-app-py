
import xlwings as xw
import os
os.chdir(os.path.dirname(__file__))
import sys
sys.path.append(os.path.dirname(__file__))


def main():

    wb = xw.Book.caller()

    ws = wb.sheets('Sheet1')
    for i in range(2, 6):
        ws.range('H' + str(i)).value = i

