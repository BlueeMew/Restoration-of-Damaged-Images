from tkinter import Tk
from ui import initializeUi

def main():
    root = Tk()
    root.title("Redo")
    root.geometry(f"{1000}x{800}") #width*height
    originalImage = None 
    processedImage = None
    initializeUi(root,originalImage,processedImage,1000,800) #Initializing UI 
    root.mainloop() #Run Tkinter event loop

if __name__ == "__main__":
    main()