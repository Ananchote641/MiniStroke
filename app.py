from flask import Flask, render_template, request
import pickle
import numpy as np

model = pickle.load(open('O:\\deploy\\MiniStroke\\model1.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def man():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def home():
    # รับค่าน้ำหนักและส่วนสูงจากฟอร์ม
    weight = float(request.form['weight'])  # น้ำหนัก
    height = float(request.form['height']) / 100  # ส่วนสูง (แปลงเป็นเมตร)

    # คำนวณ BMI
    bmi = weight / (height ** 2)

    # รับค่าตัวแปรอื่น ๆ
    age = float(request.form['age'])
    avg_glucose_level = float(request.form['avg_glucose_level'])
    hypertension = float(request.form['hypertension'])
    heart_disease = float(request.form['heart_disease'])
    ever_married = float(request.form['ever_married'])  # รับค่าเดียว
    work_type = int(request.form['work_type'])
    smoking_status = int(request.form['smoking_status'])

    mean_age = 43.229986
    mean_bmi = 29.894560
    mean_avg = 106.14399

    standard_age = 22.613575
    standard_bmi = 7.69823
    standard_avg = 45.285004

    age_standard = (age-mean_age)/standard_age
    bmi_standard = (bmi-mean_bmi)/standard_bmi
    avg_glucose_level_standard = (avg_glucose_level-mean_avg)/standard_avg



    # work
    work_type_Govt_job = 1 if work_type == 0 else 0
    work_type_Private = 1 if work_type == 1 else 0
    work_type_Self_employed = 1 if work_type == 2 else 0
    work_type_children = 1 if work_type == 3 else 0
    # กำหนดค่าอาร์เรย์ตามสถานะการสูบบุหรี่
    smoking_status_formerly_smoked = 0
    smoking_status_never_smoked = 0
    smoking_status_smokes = 0

    if smoking_status == 0:
        smoking_status_never_smoked = 1  # ไม่เคยสูบ
    elif smoking_status == 1:
        smoking_status_formerly_smoked = 1  # สูบหนัก
    else:
        smoking_status_smokes = 1  # สูบอยู่

    # แปลงค่าการแต่งงาน
    ever_married_No = 1.0 - ever_married
    ever_married_Yes = ever_married

    # กำหนดค่าของ Generation ตามอายุ
    Generation_Baby_Boomer = 1.0 if 1946 <= (2024 - age) <= 1964 else 0.0
    Generation_Gen_Alpha = 1.0 if (2024 - age) >= 2010 else 0.0
    Generation_Gen_X = 1.0 if 1965 <= (2024 - age) <= 1980 else 0.0
    Generation_Gen_Y = 1.0 if 1981 <= (2024 - age) <= 1996 else 0.0
    Generation_Gen_Z = 1.0 if 1997 <= (2024 - age) <= 2010 else 0.0

    # กำหนดค่าของน้ำหนักสุขภาพ
    healthy_weight = 1.0 if bmi < 25 else 0.0
    overweight = 1.0 if 25 <= bmi < 30 else 0.0
    obesity = 1.0 if bmi >= 30 else 0.0
    underweight = 1.0 if bmi < 18.5 else 0.0

    # สร้างอาร์เรย์ข้อมูลที่จะส่งให้โมเดล
    data = np.array([
        age_standard,
        bmi_standard,
        avg_glucose_level_standard,
        hypertension,
        heart_disease,
        ever_married_No,
        ever_married_Yes,
        work_type_Govt_job,
        work_type_Private,
        work_type_Self_employed,
        work_type_children,
        smoking_status_formerly_smoked,
        smoking_status_never_smoked,
        smoking_status_smokes,
        Generation_Baby_Boomer,
        Generation_Gen_Alpha,
        Generation_Gen_X,
        Generation_Gen_Y,
        Generation_Gen_Z,
        healthy_weight,
        obesity,
        overweight,
        underweight
    ], dtype=float).reshape(1, -1)

    print(data)
    # ทำการทำนาย
    pred = model.predict(data)

    return render_template('after.html', data=pred)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
