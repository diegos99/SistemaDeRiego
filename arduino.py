import serial

arduino_port = 'COM6'
baud = 9600
fileName = "process.csv"
ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)

def format_csv_data(stringData):
    stringData = stringData.replace("\\n", "")
    stringData = stringData.replace("\\t", ",")
    stringData = stringData.replace("\\r", "")
    stringData = stringData.replace("C", "")
    stringData = stringData.replace("b", "")
    stringData = stringData.replace("F", "")
    stringData = stringData.replace("%", "")
    stringData = stringData.replace("'", "")
    stringData = stringData.replace("lumen", "")
    stringData = stringData.replace(" ", "")
    stringData = stringData.split(",")
    return stringData

def concat_data_csv(arrayData):
    stringData = ""
    for i in range(len(arrayData)):
        # if is last element omit comma
        if i == len(arrayData) - 1:
            stringData += arrayData[i]
        else:
            stringData += arrayData[i] + ","
    return stringData

while True:
    getData=str(ser.readline())
    stringLine= concat_data_csv(format_csv_data(getData))
    print(stringLine)
    with open("process.csv", "a") as f:
        f.writelines(stringLine + "\n")
        f.close()
