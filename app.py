from flask import Flask, jsonify,render_template,request
import sqlite3
from datetime import datetime

app = Flask(__name__,template_folder="templates")
starttime =0
stoptime = 0

def get_matching_cars(car_type, start_epoch_time):
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute("SELECT licno,name,type FROM cabs WHERE type = ? AND stoptimeepoch < ?", (car_type, start_epoch_time))
    matching_cars = c.fetchall()
    conn.close()
    return matching_cars

@app.route('/')
def homepage():
    return render_template('page1.html')

@app.route('/car_details')
def car_details():
    license_number = request.args.get('lic')
    con = sqlite3.connect( 'mydb.db' )
    c = con.cursor()
    c.execute("SELECT * FROM driver WHERE licno = ?", (license_number,) )
    car_data = c.fetchone()
    con.close()
    return render_template('page4.html', car_data=car_data)

@app.route('/booking')
def booking():
    return render_template('page2.html')

@app.route('/cardata', methods=['POST'])
def get_car_data():
    car_type = request.form['carType']
    start_time = request.form['startTime']
    stop_time = request.form['stopTime']
    start_datetime_object = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
    start_epoch_time = int(start_datetime_object.timestamp())
    stop_datetime_object = datetime.strptime(stop_time, '%Y-%m-%dT%H:%M')
    stop_epoch_time = int(stop_datetime_object.timestamp())
    matching_cars = get_matching_cars(car_type, start_epoch_time)
    global start,stop
    start = start_epoch_time
    stop = stop_epoch_time
    return render_template('page1.html', cars=matching_cars)

@app.route('/update_starttime', methods=["POST"])
def update_start_time():
    licno = request.args.get('licno')
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute("UPDATE cabs SET starttimeepoch = ?, stoptimeepoch = ? WHERE licno = ?", (start, stop, licno))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/get_cabs', methods=['POST'])
def filter_cars():
    car_type = request.args.get('type')

    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()

    current_time = int(datetime.now().timestamp())
    c.execute("SELECT * FROM cabs WHERE type=? AND stoptimeepoch > ?", (car_type, current_time))
    cars = c.fetchall()
    conn.close()
    return jsonify(cabs=cars)



def check_table():
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cabs'")
    result = c.fetchone()
    conn.close()
    return result is not None

def create_table():
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cabs (
                licno VARCHAR PRIMARY KEY,
                name TEXT NOT NULL,
                type VARCHAR NOT NULL,
                starttimeepoch INTEGER,
                stoptimeepoch INTEGER
            )''')
    c.execute('''CREATE TABLE IF NOT EXISTS driver (
                licno VARCHAR PRIMARY KEY,
                name TEXT NOT NULL,
                type VARCHAR NOT NULL,
                mobilenumber TEXT,
                adhar_card_number TEXT,
                site_pay INTEGER,
                license_expiry INTEGER,
                insurance_expiry INTEGER,
                rating REAL,
                gender TEXT,
                age INTEGER,
                driver_name TEXT,
                state TEXT CHECK (state IN ('Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'))
            )''')
    conn.commit()
    conn.close()

def insert_values():
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    demo_records = [
        ('ABC123', 'Toyota Camry', 'Sedan', 1617739200, 1617742800),
        ('DEF456', 'Honda CR-V', 'SUV', 1617739200, 1617742800),
        ('GHI789', 'Ford Fiesta', 'Mini', 1617739200, 1617742800),
        ('JKL012', 'Chevrolet Silverado', 'Sports', 1617739200, 1617742800),
        ('MNO345', 'Mercedes-Benz Sprinter', 'SUV', 1617739200, 1617742800),
        ('PQR678', 'Tesla Model S', 'Sedan', 1617739200, 1617742800),
        ('STU901', 'BMW X5', 'SUV', 1617739200, 1617742800),
        ('VWX234', 'Audi A4', 'Sedan', 1617739200, 1617742800),
        ('YZA567', 'Lexus RX', 'SUV', 1617739200, 1617742800),
        ('BCD890', 'Hyundai Elantra', 'Sedan', 1617739200, 1617742800),
        ('EFG123', 'Kia Soul', 'Mini', 1617739200, 1617742800),
        ('HIJ456', 'Volvo XC90', 'SUV', 1617739200, 1617742800),
        ('KLM789', 'Tesla Model 3', 'Sedan', 1617739200, 1617742800),
        ('NOP012', 'BMW 3 Series', 'Sedan', 1617739200, 1617742800),
        ('QRS345', 'Audi Q5', 'SUV', 1617739200, 1617742800),
        ('TUV678', 'Volkswagen Golf', 'Mini', 1617739200, 1617742800),
        ('VWX901', 'Subaru Outback', 'SUV', 1617739200, 1617742800),
        ('YZA234', 'Mazda CX-5', 'SUV', 1617739200, 1617742800),
        ('BCD567', 'Nissan Altima', 'Sedan', 1617739200, 1617742800),
        ('EFG890', 'Jeep Wrangler', 'SUV', 1617739200, 1617742800)
    ]
    c.executemany('INSERT INTO cabs VALUES (?, ?, ?, ?, ?)', demo_records)
    demo_record = [
        ('ABC123', 'Toyota Camry', 'Sedan', '9876543210', '123456789012', 200, 1700000000, 1700000000, 4.5, 'Male', 35, 'John Doe', 'Maharashtra'),
        ('DEF456', 'Honda CR-V', 'SUV', '9876543211', '123456789013', 220, 1700000000, 1700000000, 4.2, 'Female', 28, 'Jane Smith', 'Karnataka'),
        ('GHI789', 'Ford Fiesta', 'Mini', '9876543212', '123456789014', 180, 1700000000, 1700000000, 4.0, 'Male', 40, 'Michael Johnson', 'Tamil Nadu'),
        ('JKL012', 'Chevrolet Silverado', 'Sports', '9876543213', '123456789015', 250, 1700000000, 1700000000, 4.7, 'Female', 32, 'Emily Brown', 'Uttar Pradesh'),
        ('MNO345', 'Mercedes-Benz Sprinter', 'SUV', '9876543214', '123456789016', 230, 1700000000, 1700000000, 4.3, 'Male', 45, 'Christopher Lee', 'Gujarat'),
        ('PQR678', 'Tesla Model S', 'Sedan', '9876543215', '123456789017', 210, 1700000000, 1700000000, 4.6, 'Female', 29, 'Amanda Wilson', 'West Bengal'),
        ('STU901', 'BMW X5', 'SUV', '9876543216', '123456789018', 240, 1700000000, 1700000000, 4.4, 'Male', 38, 'Robert Taylor', 'Maharashtra'),
        ('VWX234', 'Audi A4', 'Sedan', '9876543217', '123456789019', 215, 1700000000, 1700000000, 4.1, 'Female', 31, 'Jennifer Davis', 'Kerala'),
        ('YZA567', 'Lexus RX', 'SUV', '9876543218', '123456789020', 235, 1700000000, 1700000000, 4.3, 'Male', 33, 'Matthew Thomas', 'Uttar Pradesh'),
        ('BCD890', 'Hyundai Elantra', 'Sedan', '9876543219', '123456789021', 205, 1700000000, 1700000000, 3.9, 'Female', 27, 'Elizabeth Martinez', 'Karnataka'),
        ('EFG123', 'Kia Soul', 'Mini', '9876543220', '123456789022', 190, 1700000000, 1700000000, 3.8, 'Male', 41, 'Daniel Garcia', 'Telangana'),
        ('HIJ456', 'Volvo XC90', 'SUV', '9876543221', '123456789023', 225, 1700000000, 1700000000, 4.5, 'Female', 30, 'Sarah Rodriguez', 'Maharashtra'),
        ('KLM789', 'Tesla Model 3', 'Sedan', '9876543222', '123456789024', 215, 1700000000, 1700000000, 4.4, 'Male', 36, 'Christopher Brown', 'Gujarat'),
        ('NOP012', 'BMW 3 Series', 'Sedan', '9876543223', '123456789025', 210, 1700000000, 1700000000, 4.2, 'Female', 26, 'Lisa Hernandez', 'Uttar Pradesh'),
        ('QRS345', 'Audi Q5', 'SUV', '9876543224', '123456789026', 230, 1700000000, 1700000000, 4.3, 'Male', 37, 'David Lopez', 'Tamil Nadu'),
        ('TUV678', 'Volkswagen Golf', 'Mini', '9876543225', '123456789027', 195, 1700000000, 1700000000, 3.7, 'Female', 25, 'Mary Martinez', 'Karnataka'),
        ('VWX901', 'Subaru Outback', 'SUV', '9876543226', '123456789028', 235, 1700000000, 1700000000, 4.2, 'Male', 34, 'Patricia Wright', 'Maharashtra'),
        ('YZA234', 'Mazda CX-5', 'SUV', '9876543227', '123456789029', 230, 1700000000, 1700000000, 4.1, 'Female', 28, 'Joseph Anderson', 'Tamil Nadu'),
        ('BCD567', 'Nissan Altima', 'Sedan', '9876543228', '123456789030', 200, 1700000000, 1700000000, 3.8, 'Male', 39, 'Jessica Wilson', 'Uttar Pradesh'),
        ('EFG890', 'Jeep Wrangler', 'SUV', '9876543229', '123456789031', 240, 1700000000, 1700000000, 4.4, 'Female', 32, 'Thomas Taylor', 'Gujarat')
    ]
    c.executemany('INSERT INTO driver VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', demo_record)
    conn.commit()
    conn.close()

@app.route("/aboutme")
def aboutme():
    return render_template('page3.html')





if __name__ == "__main__":
    start = 0
    stop = 0
    if not check_table():
        create_table()
        insert_values()
    app.run(debug=True)