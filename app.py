import cv2
import numpy as np
from keras.models import load_model
import tkinter as tk
model = load_model('xss.h5')
def convert_to_ascii(sentence):
    sentence_ascii = []
    for i in sentence:
        if (ord(i) <= 8222):
            if (ord(i) == 8217):
                sentence_ascii.append(134)
            if (ord(i) == 8221):
                sentence_ascii.append(129)
            if (ord(i) == 8220):
                sentence_ascii.append(130)
            if (ord(i) == 8216):
                sentence_ascii.append(131)
            if (ord(i) == 8217):
                sentence_ascii.append(132)
            if (ord(i) == 8211):
                sentence_ascii.append(133)
            if (ord(i) <= 128):
                sentence_ascii.append(ord(i))
            else:
                pass
    zer = np.zeros((10000))
    for i in range(len(sentence_ascii)):
        zer[i] = sentence_ascii[i]
    zer.shape = (100, 100)
    return zer
def predict_xss(user_input):
    input_ascii = convert_to_ascii(user_input)
    x = np.asarray(input_ascii, dtype='float')
    input_image = cv2.resize(x, dsize=(100, 100), interpolation=cv2.INTER_CUBIC)
    input_image /= 128
    input_data = input_image.reshape(1, 100, 100, 1)
    prediction = model.predict(input_data)
    if prediction > 0.5:
        return "XSS Attack"
    else:
        return "No Chance of XSS Attack!"
def submit():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()
    user_input = entry.get()
    output = predict_xss(user_input)
    label = tk.Label(root, text=output, font=("Helvetica", 16), bg="black", fg="white")
    label.pack(pady=20)
root = tk.Tk()
root.title("XSS Attack Detection")
root.geometry("600x600")
root.configure(background="black")
root.resizable(0, 0)
label = tk.Label(root, text="Enter the input to check for XSS Attack", font=("Helvetica", 16), bg="black", fg="white")
label.pack(pady=20)
entry = tk.Entry(root, width=50)
entry.pack(pady=20)
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack(pady=20)
root.mainloop()
