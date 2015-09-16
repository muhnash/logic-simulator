# usr/bin/python3.4 
# Digital Logic Simulator

wire_num=0
gate_num=0
class Wire():
    def __init__(self):
        global wire_num
        self.num=wire_num+1
        self.name='wire'+str(self.num)
        self.value=None
        wire_num=wire_num+1

    def set_name(self,wire_name):
        if type(wire_name)!=str:
            print("INPUT TYPE ERROR , String EXPECTED !!")
        else:
            self.name= wire_name

    def set_value(self,digital_in):
        if type(digital_in)!=int and digital_in !=None :
            print("INPUT TYPE ERROR , Integer EXPECTED !!")
        elif digital_in==1:
            self.value=digital_in
        elif digital_in==0:
            self.value=0
        else:
            self.value=None

    def get_name(self):
        return  self.name

    def get_value(self):
        return self.value
class Gate():
    'BASE Class for all logic gates'
    def __init__(self):
        global gate_num
        self.name='gate'+str(gate_num+1)
        self.inputs=[]
        self.output=Wire()
        gate_num+=gate_num+1

    def set_name(self,gate_name):   # has no use !
        self.name=gate_name

    def set_inputs(self,*args:Wire):
        self.inputs=args[:]

    def set_output(self,out_wire: Wire):   # to assign a wire for the output
                                           # calc_output() then uses set_value() from wire class
        self.output=out_wire

    def calc_output(self):
        pass

    def get_output_wire(self):
        return self.output

    def get_output_value(self):
        return  self.output.get_value()


class AND(Gate):
    def calc_output(self):
        digital_op=1
        for wire in self.inputs:
            digital_op = digital_op and wire.get_value()
        self.output.set_value(digital_op)


class OR(Gate):
     def calc_output(self):
        digital_op=0
        for wire in self.inputs:
            digital_op = digital_op or wire.get_value()
        self.output.set_value(digital_op)


class NOT(Gate):
    def set_inputs(self,wire_input:Wire):
        self.inputs.append(wire_input)

    def calc_output(self):
        digital_op=None
        if self.inputs[0].get_value()==0:
            digital_op=1
            self.output.set_value(digital_op)
        elif self.inputs[0].get_value()==1:
            digital_op=0
            self.output.set_value(digital_op)
        else:
            self.output.set_value(digital_op)      # BUG : wire.set_value() doesn't accept "None" value !!
            pass


def file_to_list(file_name):
    'takes a file name and return a list of lines within, no blank lines , no leading/trailing whitespaces  '
    lines_list = []
    f = open(str(file_name), 'r')
    for line in f:
        if line.strip():  # False : the line is empty
            lines_list.append(line.strip())  # line.strip() : strips any spaces before/after the string
    f.close()
    return lines_list


def split_list(lines_list:list):
    'takes lines_list and s'
    split_index=lines_list.index('---')
    values_list=lines_list[0:split_index]
    gates_list=lines_list[split_index+1 : len(lines_list)]
    return values_list,gates_list


def gates_listing(gate_list :list):
    'takes a list of strings of for spaced fields , turns every string to a list of 4 elements ,then returns a list of lists'
    final_list=[]
    for line in gate_list:
        copy=line
        argument_list=[]
        while len(argument_list)<=4:
            if ' 'in copy:
                x=copy.find(' ')
                element=copy[0:x]
                argument_list.append(element)
                copy=copy[x+1:len(copy)]
            else:
                element=copy
                argument_list.append(element)
        final_list.append(argument_list)
    return final_list


def list_to_dic(input_list):
    temp=[]
    dic={}
    for line in input_list:
        for x in line.split('='):
            temp.append(x)
    i=0
    while i<len(temp):
        dic[str(temp[i])]=temp[i+1]
        i=i+2
    return dic



def main():
####### PARSING THE INPUT FILE ################
    full_list=file_to_list('input_file.txt')    # full List : list of all lines in the file , No blank lines ..

    values_lines=split_list(full_list)[0]        # values lines: list of values lines in the file
    gates_lines=split_list(full_list)[1]         # gates lines : list of gates/instructions lines in the file

    instructions_list=gates_listing(gates_lines)    # list of lists , each sub-list = one instruction line .. containing the 5 fields
    wires_dictionary=list_to_dic(values_lines)      # turning the values_list to a dictionary , Keys=> wire_names , values => wire_values
##################################################
################ OPERATING ######################


    objects_list=[]  # list of all gates objects

    for line in instructions_list:
        print(line)
        if line[1].upper()=='AND':
            gate_input1=Wire()
            gate_input2=Wire()
            gate_output=Wire()

            gate_input1.set_name(line[0])
            gate_input2.set_name(line[2])
            gate_output.set_name(line[4])

            #print(gate_output.get_name())
            #print(wires_dictionary.keys())
            if line[0] in wires_dictionary.keys():
                #print(int(wires_dictionary[line[0]]))
                gate_input1.set_value( int(wires_dictionary[line[0]] ) )
                print(gate_input1.get_value())

            if line[2] in wires_dictionary.keys():
                gate_input2.set_value( int(wires_dictionary[line[2]] ) )
                print(gate_input2.get_value())

            gate_object=AND()

            gate_object.set_inputs(gate_input1,gate_input2)
            gate_object.set_output(gate_output)
            gate_object.calc_output()
            wires_dictionary[line[4]]=gate_object.get_output_value()  #UPDATING THE WIRES DICTIONARY

            objects_list.append(gate_object)

        elif line[1].upper()=='OR':
            pass                            # to Update
        elif line[1].upper()=='NOT':
            pass                            # to Update


    print('Answer => ' + str(objects_list[-1].get_output_value()))
    print(wires_dictionary)
    
if __name__ == '__main__':main()
