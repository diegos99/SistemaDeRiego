# Proyecto Final de Sistemas Inteligentes
# Autor: Aníbal Andrés Higueros Hernández
# Autor: Juan Diego Vega Ruiz
# Autor: Javier Jose Alvarez Flores
# Fecha: 30/04/2020

# Ideal temperature is 25 - 30 degrees Celsius
# Ideal ground humidity is 50 - 60 %
# Maximum temperature in Gutemala is 35 degrees Celsius
# Ideal ambiental humidity is 50 - 60%
# Maximun ambiental humidity is 100%
# Ideal LDR value is 60%
# Maximun LDR value is 100%

# Temperature                             | Linguistic Variable
# Range 1: 0 - 25                         | Low
# Range 2: 25 - 35                        | medium
# Range 3: 35 - 45                        | high

# Ambiental Humidity                      | Linguistic Variable
# Range 1: 0 - 50                         | low
# Range 2: 50 - 60                        | medium
# Range 3: 60 - 100                       | high

# LDR                                     | Linguistic Variable
# Range 1: 0 - 30                         | low
# Range 2: 30 - 60                        | medium
# Range 3: 60 - 100                        | high

# Ground Humidity                         | Linguistic Variable
# Range 1: 0 - 50                         | low
# Range 2: 50 - 60                        | medium
# Range 3: 60 - 100                       | high

# Irrigate Plant
# Value 1                                 | Irrigate
# Value 0                                 | Do not irrigate

from numpy import array
import matplotlib.pyplot as plt
from numpy.lib.financial import irr
import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import os
import time

# importar el archivo del dataset previamente creado
dataset = pd.read_csv(
    "data.csv", encoding='utf-8', header=None)

# Define function to split values from csv


def split_value(stringLine):
    stringLine.replace("'", "")
    stringLine.replace("\\n", "")
    arrayData = stringLine.split(",")
    # conver value to float
    arrayData = [float(i) for i in arrayData]
    return arrayData

# Asign the data to the linguistic variables


humidity = array(dataset.iloc[:, 1].values)
temperature = array(dataset.iloc[:, 2].values)
ldr = array(dataset.iloc[:, 3].values)
humidity_ground = array(dataset.iloc[:, 4].values)
irrigate = array(dataset.iloc[:, 5].values)

# Fuzzy Variables

temperature_fuzzy = ctrl.Antecedent(np.arange(0, 45, 1), 'temperature')

temperature_fuzzy['low'] = fuzz.trimf(temperature_fuzzy.universe, [0, 0, 25])
temperature_fuzzy['medium'] = fuzz.trimf(
    temperature_fuzzy.universe, [25, 35, 35])
temperature_fuzzy['high'] = fuzz.trimf(
    temperature_fuzzy.universe, [35, 40, 45])
# temperature_fuzzy.view()

humidity_fuzzy = ctrl.Antecedent(np.arange(0, 100, 1), 'humidity')

humidity_fuzzy['low'] = fuzz.trimf(humidity_fuzzy.universe, [0, 0, 50])
humidity_fuzzy['medium'] = fuzz.trimf(humidity_fuzzy.universe, [50, 60, 60])
humidity_fuzzy['high'] = fuzz.trimf(humidity_fuzzy.universe, [60, 100, 100])
# humidity_fuzzy.view()

ldr_fuzzy = ctrl.Antecedent(np.arange(0, 100, 1), 'ldr')

ldr_fuzzy['low'] = fuzz.trimf(ldr_fuzzy.universe, [0, 0, 30])
ldr_fuzzy['medium'] = fuzz.trimf(ldr_fuzzy.universe, [30, 60, 60])
ldr_fuzzy['high'] = fuzz.trimf(ldr_fuzzy.universe, [60, 100, 100])
# ldr_fuzzy.view()

humidity_ground_fuzzy = ctrl.Antecedent(
    np.arange(0, 100, 1), 'humidity_ground')

humidity_ground_fuzzy['low'] = fuzz.trimf(
    humidity_ground_fuzzy.universe, [0, 0, 50])
humidity_ground_fuzzy['medium'] = fuzz.trimf(
    humidity_ground_fuzzy.universe, [50, 60, 60])
humidity_ground_fuzzy['high'] = fuzz.trimf(
    humidity_ground_fuzzy.universe, [60, 100, 100])
# humidity_ground_fuzzy.view()

irrigate_fuzzy = ctrl.Consequent(np.arange(0, 100, 1), 'irrigate')
irrigate_fuzzy['irrigate'] = fuzz.trimf(irrigate_fuzzy.universe, [0, 50, 50])
irrigate_fuzzy['do_not_irrigate'] = fuzz.trimf(
    irrigate_fuzzy.universe, [50, 100, 100])
# irrigate_fuzzy.view()

# Define rules for fuzzy logic
# Rule for temperature

rule_1 = ctrl.Rule(humidity_fuzzy['medium'] | humidity_ground_fuzzy['medium'] & temperature_fuzzy['medium'] & ldr_fuzzy['medium'], irrigate_fuzzy['irrigate'])
rule_2 = ctrl.Rule(humidity_ground_fuzzy['high'] & temperature_fuzzy['medium'], irrigate_fuzzy['do_not_irrigate'])
rule_3 = ctrl.Rule(ldr_fuzzy['high'] & humidity_fuzzy['medium'], irrigate_fuzzy['do_not_irrigate'])
rule_4 = ctrl.Rule(ldr_fuzzy['high'] | humidity_fuzzy['high'] | humidity_ground_fuzzy['high'], irrigate_fuzzy['do_not_irrigate'])
rule_5 = ctrl.Rule(temperature_fuzzy['medium'] & humidity_fuzzy['medium'] | humidity_ground_fuzzy['medium'], irrigate_fuzzy['irrigate'])
rule_6 = ctrl.Rule(humidity_fuzzy['medium'] | humidity_ground_fuzzy['medium'] | humidity_ground_fuzzy['low'], irrigate_fuzzy['irrigate'])
rule_7 = ctrl.Rule(humidity_fuzzy['low'] | humidity_ground_fuzzy['low'], irrigate_fuzzy['irrigate'])
rule_8 = ctrl.Rule(humidity_fuzzy['high'] | humidity_ground_fuzzy['high'], irrigate_fuzzy['do_not_irrigate'])
rule_9 = ctrl.Rule(humidity_fuzzy['medium'] | humidity_ground_fuzzy['medium'], irrigate_fuzzy['irrigate'])
rule_10 = ctrl.Rule(temperature_fuzzy['high'] & humidity_fuzzy['medium'] | humidity_ground_fuzzy['medium'], irrigate_fuzzy['do_not_irrigate'])
rule_11 = ctrl.Rule(temperature_fuzzy['high'] | humidity_fuzzy['high'] | humidity_ground_fuzzy['high'], irrigate_fuzzy['do_not_irrigate'])
rule_12 = ctrl.Rule(ldr_fuzzy['high'] | humidity_fuzzy['high'] | humidity_ground_fuzzy['high'], irrigate_fuzzy['do_not_irrigate'])

while True:
    # Do a task every 5 seconds
    # read file and split values
    with open('process.csv', 'r') as file:
        for line in file:
            pass
        last_line = line

        # split values
        arrayData = split_value(last_line)

        # Fuzzycation of data
        rule_list = ctrl.ControlSystem([rule_1, rule_2, rule_3, rule_4, rule_5, rule_6, rule_7, rule_8, rule_9, rule_10, rule_11, rule_12])
        fs = ctrl.ControlSystemSimulation(rule_list)

        # FS = fuzzy system
        test_humidity = arrayData[0]
        test_temperature = arrayData[1]
        test_ldr = arrayData[5]
        test_ground_humidity = arrayData[7]

        fs.input['humidity'] = test_humidity
        fs.input['temperature'] = test_temperature
        fs.input['ldr'] = test_ldr
        fs.input['humidity_ground'] = test_ground_humidity

        fs.compute()

        print(fs.output['irrigate'])
        irrigate_fuzzy.view(sim=fs)
        plt.show()

        # Wait for 5 seconds
        time.sleep(4)
