import json
from difflib import get_close_matches

data = json.load(open("data.json"))

def translate(dictData):
    # add to accept all type of word
    dictData = dictData.lower()
    if dictData in data:
        return data[dictData]
    elif dictData.title() in data: #if user entered "texas" this will check for "Texas" as well.
        return data[dictData.title()]
    # Check matches answer of data
    elif len(get_close_matches(dictData, data.keys())) > 0:
        answer = input("Did you mean [%s] instead ? Y or N: "
                     % get_close_matches(dictData, data.keys())[0])
        if answer == "Y" or answer == "y":
            return data[get_close_matches(dictData, data.keys())[0]]
        elif answer == "N" or answer == "n":
            return "The word does't exist, please double click on the word"
        else:
            return "We don't understand you question...Sorry"
    else:
        return "The word does't exist, please double click on the word"


if __name__ == '__main__':
    while True:
        word = input("Enter word: ")
        print("Press E to Exit \n")
        if word == "E":
            break
        else:
            #improve output
            output = translate(word)
            if type(output) == list:
                for item in output:
                    print(item)
            else:
                print(output)
            if word == "E":
                break
