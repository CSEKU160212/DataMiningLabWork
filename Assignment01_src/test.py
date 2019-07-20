import openpyxl
wb = openpyxl.load_workbook('example.xlsx')
sheet = wb.get_sheet_by_name('Sheet1')

stimulusTimes = [1, 2, 3]
reactionTimes = [2.3, 5.1, 7.0]

for i in range(len(stimulusTimes)):
    sheet['A' + str(i + 6)].value = stimulusTimes[i]
    sheet['B' + str(i + 6)].value = reactionTimes[i]

wb.save('example.xlsx')