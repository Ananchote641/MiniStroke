import pickle
import numpy as np

# โหลดโมเดล
with open('O:\\MiniProject\\MODEL\\model1.pkl', 'rb') as file:
    model = pickle.load(file)

# ตรวจสอบว่า model มี method predict
print(type(model))  # ตรวจสอบชนิดของ model ว่าเป็น class ที่ถูกต้องหรือไม่
if hasattr(model, 'predict'):
    print("Model is valid and has predict method.")
else:
    print("Model does not have predict method.")

# ตัวอย่างข้อมูลใหม่ (ต้องมีรูปแบบเป็น 2D array)
new_data = np.array([[15.0, 17.4, 74.83, 0, 0, False, True, True, False, False, False,
        False, False, True, True, False, False, False, True, False,
        False, False, False, False, True, False, False, False, True]])
        
new_data1 = np.array([[0.12250538868794554,1.5596581573199189,-0.05566182599577174,0.0,0.0,0.0,1.0,0.0,1.0,0.0,0.0,0.0,
0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0]])

# ทำการพยากรณ์    
if hasattr(model, 'predict'):
    predictions = model.predict(new_data1)
    print(predictions)
else:
    print("Error: The model is not valid.")
