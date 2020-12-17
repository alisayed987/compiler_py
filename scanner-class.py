class LexicalAnalyzer(object):

    def __init__(self, reserved_words=None, special_symbols=None):
        if reserved_words is None:
            self.reserved_words = ["if", "then", "else", "end", "repeat",
                                   "until", "read", "write"]
        if special_symbols is None:
            self.special_symbols = ["+", "-", "*", "/", "=",
                                    "<", "(", ")", ";" ,">"]
        self.token = []
        self.set_value = ""
        self.set_type = ""
        self.set_number = "0123456789"
        self.set_symbol = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.current_position = 0
        self.current_state = 1
        

    def take_token(self, next_state):
       
        if self.current_state == 1:
            if next_state == "{":
                self.current_state = 2
            elif next_state == ":":
                self.set_type = " >> ASSIGNMENT"
                self.current_state = 3
            elif next_state in self.special_symbols:
                self.set_type = " >> SPECIAL SYMBOL"
                self.set_value = next_state
                self.current_state = 6
            elif next_state in self.set_symbol :
                self.set_type = " >> IDENTIFIER"
                self.set_value = next_state
                self.current_state = 4
            elif next_state in self.set_number:
                self.set_type = " >> NUMBER"
                self.set_value = next_state
                self.current_state = 5
            elif next_state != " " and next_state != "\n":
                self.current_state = -1
        elif self.current_state == 2:
            if next_state == "}":
                self.current_state = 1
                self.set_value = ""
        elif self.current_state == 3:
            if next_state == "=":
                self.set_value = ":="
                self.current_state = 6
        elif self.current_state == 4:
            if next_state in self.set_symbol:
                self.set_value += next_state
            else:
                
                self.current_state = 6
                if self.set_value in self.reserved_words:
                    self.set_type = " >> RESERVED WORD"
                    self.current_position -= 1
        elif self.current_state == 5:
            if next_state in self.set_number :
                self.set_value += next_state
            else:
                self.current_state = 6
                self.current_position -= 1

        elif self.current_state == 6:
            self.token.append(self.set_value + self.set_type)
            
            self.current_position -= 1
            self.current_state = 1
        self.current_position += 1

    def file_process(self, in_file="tiny_sample_code.txt", out_file="scanner_output.txt"):
        input_file = open(in_file ,"r")
        first_line = 1
        for line in input_file.readlines():
            line = line + " "
            
            end = len(line[:-1])
            while self.current_position <= end:
                self.take_token(line[self.current_position])
            self.current_position = 0
            if self.current_state < 0:
                break
            first_line += 1
        input_file.close()
        if self.current_state < 0:
            print ("THERE IS AN ERROR !!! ", first_line)
            return
        output_file = open(out_file, 'w')
        for i in self.token:
            
            output_file.write(i+"\n")
            
        output_file.close()
        print ("PROCESS RUN SUCCESSFULLY !!!")


X = LexicalAnalyzer()
X.file_process()
