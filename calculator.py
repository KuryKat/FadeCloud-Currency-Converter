import sys

currencies = {
    'clouds'    : '100',
    'souls'     : '250b',
    'gems'      : '2.5b',
    'knight'    : '2.5m',
    'warrior'   : '1.25m',
    'berserker' : None,
    'overlord'  : None
}

multipliers = {
    'd': 1000000000000000000000000000000000,
    'n': 1000000000000000000000000000000,
    'o': 1000000000000000000000000000,
    'S': 1000000000000000000000000,
    's': 1000000000000000000000,
    'Q': 1000000000000000000,
    'q': 1000000000000000,
    't': 1000000000000,
    'b': 1000000000,
    'm': 1000000,
    'k': 1000
}

def concat_with_comma(words):
    return ', '.join(words[:-2]) + (', ' if len(words) > 2 else '') + ' and '.join(words[-2:])

if(len(sys.argv) > 1 and len(sys.argv) <= 4):
    inputType  = sys.argv[1]
    value      = sys.argv[2]
    outputType = sys.argv[3]
else:
    currencies_str = concat_with_comma(['"{}"'.format(k) for k in currencies.keys()])
    multipliers_list = ['"1{}"'.format(k) for k in multipliers.keys()]
    multipliers_list.reverse()
    multipliers_str = concat_with_comma(multipliers_list)
    inputType  = input('What is the input currency?\n  - You can use {}\n=> '.format(currencies_str))
    value      = input('What is the value to convert?\n  - You can use {}\n=> '.format(multipliers_str))
    outputType = input('What is the output currency?\n  - You can use {}\n=> '.format(currencies_str))

def convertNumber(value):
    try:
        number = float(value)
    except ValueError:
        number = float(value[:-1])

    last_char = value[-1]
    if last_char in multipliers:
        number *= multipliers[last_char]

    return number

def formatNumber(number):
    for suffix, factor in multipliers.items():
        if number >= factor:
            formatted_number = str(int(round(number / factor, 1))) + suffix
            break
    else:
        formatted_number = str(int(round(number, 1)))

    return formatted_number

class InputError(Exception):
    pass

class ConversionError(Exception):
    pass

def rule_of_three(a, b, c):
    # a : b = c : x
    return (b * c) / a

def convertValues(value, input, output):
    if(input in currencies and output in currencies):
        inputRate  = currencies[input]
        outputRate = currencies[output]
        
        if(inputRate is None):
            raise ConversionError("There is still NO value for this Currency: {}".format(input))
        elif(outputRate is None):
            raise ConversionError("There is still NO value for this Currency: {}".format(output))
        
        inputRate  = convertNumber(inputRate)
        outputRate = convertNumber(outputRate)
        value = convertNumber(value)
        
        result = rule_of_three(inputRate, outputRate, value)
        
        return formatNumber(result)
    else:
        raise InputError("You need to input a valid currency!")

try:
    result = convertValues(value, inputType, outputType)
    
    print("================================")
    print("RESULT: {} {} = {} {}".format(value, inputType, result, outputType))
    print("================================")
except Exception as err:
    print("=================================================================")
    print("** ERROR: {} **".format(err))
    print("=================================-===============================")