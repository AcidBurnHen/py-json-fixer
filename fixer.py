import json
import re
    
broken_json = '{adk: "oko", "ada": 1 piip: 3, 6: 1, {"ab": "cd", 1: 0}{"ab": "cd", 1: 0}[],}'

valid_json = """{
  "name": "John Doe",
  "age": 28,
  "gender": "male",
  "city": "New York",
  "country": "USA",
  "email": "johndoe@example.com",
  "phone": "+1 555-123-4567",
  "interests": [
    "hiking",
    "photography",
    "cooking"
  ],
  "education": {
    "degree": "Bachelor's",
    "major": "Computer Science",
    "university": "XYZ University"
  }
}"""

# Wrong patters to work on later
#   [ { ] }

class JsonFixer():
    def __init__(self):
        # Keys
        self.ERR = "error"
        self.POS = "position"

        # Errors 
        self.UNESC = "Unescaped character: "
        self.WRPOS = " at wrong position"


    def rindex_list(self, list, char):
        return len(list) - list[::-1].index(char) - 1 
    
    def indexes_list(self, list, char):
        return [index for index, item in enumerate(list) if item == char]
    
    def escape_valid_chars(self, json_str):
        value = re.findall(r"\"([^\"]+)\"", json_str, flags=re.I)
        mock_value = value
        for words in value.reverse():
            words = words.split(" ")
            for word in words:
                symbol = re.search(r"([^0-9a-z\"])", word, flags=re.I)
                if symbol and symbol.group(1) is not None:
                    pass

        pass

    def find_errors_in_json(self, json_str):
        fixed_json = None

        # Position of text 
        index = 0
        # All errors to be iterated and fixed
        errors = []

        curly_stack = []
        square_stack = []
        value_stack = []
        comma_stack = []
        colon_stack = []
        value_count = 0
        quote_stack = []
        for char in json_str:
            index += 1
            if char == "{":
                curly_stack += char
            elif char == "}":
                curly_stack += char

                if curly_stack.rindex("{") is not None:
                    del curly_stack[curly_stack.rindex("{")]
                    del curly_stack[curly_stack.rindex(char)]
            elif char == '\"':
                quote_stack.append(char)

                if len(quote_stack) == 2:
                    if len(value_stack) > 0 and value_stack[self.rindex_list(value_stack, char) - 1] ==  r"\\":
                        del quote_stack[1]

                        value_stack += char
                    else:
                        quote_stack.clear()
                        value_count += 1
            elif char == ",":
                if value_count == 0 and len(quote_stack) == 1: 
                    pass
                if value_count != 2:
                    errors.append({self.ERR: f", {self.WRPOS}", self.POS: index})
                    value_count = 0
            elif char == ":":
                if value_count != 1: 
                    errors.append({self.ERR: f": {self.WRPOS}", self.POS: index})
            elif char == '\'':
                if len(value_stack) > 0 and value_stack[self.rindex_list(value_stack, char) - 1] ==  r"\\":
                    value_stack += char
                else:
                    errors.append({self.ERR: f"{self.UNESC} \' ", self.POS: index})



        return fixed_json



