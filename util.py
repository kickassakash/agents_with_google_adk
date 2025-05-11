#helper funciton which will help load custom instruction from text files
#to the agents
import os

def load_instruction_from_file(fileName: str,definstruction='Default Instruction') -> str:
    instruction = definstruction
    try:
        filepath = os.path.join(os.path.dirname(__file__),fileName)
        with open(filepath,mode='r',encoding='utf-8') as f:
            instruction = f.read()
        print(f"successfully loaded instruction from {fileName}")
    except FileNotFoundError:
        print(f"given filename : {fileName} is not found , going with default instruction")
    except Exception as e:
        print(f"facing exception {e} while loading {fileName}, using default")
    
    return instruction