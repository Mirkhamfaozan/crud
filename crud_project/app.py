from flask import Flask, request, jsonify #library #json = formatdata
from flask_sqlalchemy import SQLAlchemy #library #jsonify mengonversi objek python ke json

app = Flask(__name__) #baris kode yang membuat objek Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # Nama database SQLite
db = SQLAlchemy(app) # untuk menginisialisasi objek SQLAlchemy dalam konteks aplikasi Flask.

class Data(db.Model): #kelas Python yang disebut "Data
    id = db.Column(db.Integer, primary_key=True) #kolom dalam tabel yang sesuai dengan atribut "id" dalam model "Data."
    nama = db.Column(db.String(100), nullable=False) #definisi kolom kedua dalam tabel yang sesuai 
    #                                                dengan atribut "nama" dalam model "Data." teks (string) dengan panjang maks 100 karakter. 
    alamat = db.Column(db.String(200), nullable=False) #i kolom ketiga dalam tabel yang sesuai dengan atribut "alamat" dalam model "Data.

@app.route('/data', methods=['GET']) #decorator yang digunakan untuk menghubungkan fungsi di bawahnya dengan rute tertentu
def get_data():       #fungsi untuk menampilkan data     # hanya permintaan GET yang akan diizinkan pada rute ini
    data_list = Data.query.all() #model Data untuk mengakses tabel yang Anda ingin ambil. #tanda kurung untuk menampung data
    data_json = [{'id': data.id, 'nama': data.nama, 'alamat': data.alamat} for data in data_list]
    return jsonify({'data': data_json}) #Ini adalah fungsi bawaan Flask yang digunakan untuk mengambil objek Python,

@app.route('/data', methods=['POST'])
def create_data():
    data = request.get_json()
    if 'nama' in data and 'alamat' in data:
        new_data = Data(nama=data['nama'], alamat=data['alamat'])
        db.session.add(new_data) #bagian dari SQLAlchemy dan digunakan untuk menambahkan data baru ke database.
        db.session.commit() #mengonfirmasi bahwa data sudah ditambahkan
        return jsonify({'message': 'Data created successfully'}), 201
    else:
        return jsonify({'error': 'Nama dan Alamat diperlukan'}), 400

@app.route('/data/<int:id>', methods=['PUT'])
def update_data(id):
    data = Data.query.get(id)
    if data:
        data_json = request.get_json() #untuk mengambil data dalam format JSON yang dikirim oleh klien sebagai bagian dari permintaan HTTP
        data.nama = data_json['nama']
        data.alamat = data_json['alamat']
        db.session.commit()
        return jsonify({'message': 'Data updated successfully'})
    else:
        return jsonify({'error': 'Data tidak ditemukan'}), 404

@app.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    data = Data.query.get(id)
    if data:
        db.session.delete(data)
        db.session.commit()
        return jsonify({'message': 'Data deleted successfully'})
    else:
        return jsonify({'error': 'Data tidak ditemukan'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)