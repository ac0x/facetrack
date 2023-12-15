import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import face_recognition
from firebase_admin import credentials, initialize_app, storage, db



def save_student():
    student_id = entry_id.get()
    student_name = entry_name.get()
    student_department = entry_department.get()
    student_index = entry_index.get()

    try:
        image_path = entry_image_path.get()
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]

        bucket = storage.bucket()
        blob = bucket.blob(f'Images/{student_id}.jpg')
        blob.upload_from_filename(image_path)

        ref = db.reference(f'Students')

        data = {
            student_id:
                {
                    "name": student_name,
                    "smjer": student_department,
                    "index": student_index,
                    "total_attendance": 1,
                    "standing": "6",
                    "year": 4,
                    "last_attendance_time": "2023-11-29 01:53:30",
                    #'encode': encode.tolist(),
                },
        }

        ref.set(data)

        messagebox.showinfo("Uspeh", f"Podaci za studenta {student_name} su sačuvani.")
    except Exception as e:
        messagebox.showerror("Greška", f"Nije moguće sačuvati podatke: {str(e)}")


def browse_image():
    file_path = filedialog.askopenfilename()
    entry_image_path.delete(0, tk.END)
    entry_image_path.insert(0, file_path)

# Inicijalizacija Firebase
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred, {
    'storageBucket': "facetrack-80ed9.appspot.com",
    'databaseURL': "https://facetrack-80ed9-default-rtdb.europe-west1.firebasedatabase.app/"
})


#gui
root = tk.Tk()
root.title("Unos podataka o studentu")
#id
label_id = tk.Label(root, text="ID studenta:")
label_id.pack()

entry_id = tk.Entry(root)
entry_id.pack()

#index
label_index = tk.Label(root, text="Index studenta:")
label_index.pack()

entry_index = tk.Entry(root)
entry_index.pack()

#ime
label_name = tk.Label(root, text="Ime studenta:")
label_name.pack()

entry_name = tk.Entry(root)
entry_name.pack()

#smjer
label_department = tk.Label(root, text="Smjer:")
label_department.pack()

entry_department = tk.Entry(root)
entry_department.pack()

#slika
label_image = tk.Label(root, text="Slika studenta:")
label_image.pack()

entry_image_path = tk.Entry(root)
entry_image_path.pack()

browse_button = tk.Button(root, text="Pretraži", command=browse_image)
browse_button.pack()

#cuvanje
save_button = tk.Button(root, text="Sačuvaj", command=save_student)
save_button.pack()


root.mainloop()
