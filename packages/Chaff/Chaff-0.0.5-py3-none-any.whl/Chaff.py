import os
from clear import clear

def Chaff():
    clear()

    print("CREATING CHAFF")
    try:
        with open("CHAFF", "wb") as file:
            while True:
                file.write(b"0" * 65535)

    except:
        pass

    print("REMOVING CHAFF")
    os.remove("CHAFF")
    print("DONE!")
    
if __name__ == "__main__":
    Chaff()
