from pedatren import Pedatren, cetakExcel
import xlrd
from app import logger

api = Pedatren()

def allData():
    data = api.all_pelajar()
    temp = []
    temp.append([
        'NOMOR INDUK', 'UUID', 'NAMA LENGKAP', 'ID PENDIDIKAN',
        'ID LEMBAGA', 'KELAS', 'JURUSAN', 'TANGGAL MASUK LEMBAGA',
        ])
    for i in data:
        data_pelajar = (
            None,
            i.get('uuid'),
            i.get('nama_lengkap'), i.get('pendidikan').get('id'), i.get('pendidikan').get('id_lembaga'),
            i.get('pendidikan').get('kelas'), i.get('pendidikan').get('jurusan'), i.get('pendidikan').get('tanggal_mulai'),  
        )
        temp.append(data_pelajar)
    cetakExcel(temp)
    
def updateNomorInduk():
    book = xlrd.open_workbook("data_siswa.xlsx")
    sheet = book.sheet_by_index(0)
    for i in range(1, sheet.nrows):
        induk = sheet.cell(i,0).value
        uuid = sheet.cell(i,1).value
        nama = sheet.cell(i,2).value
        id_pendidikan = sheet.cell(i,3).value
        id_lembaga = sheet.cell(i,4).value
        tanggal_masuk = sheet.cell(i,7).value
        updatePelajar = api.updateInduk(
            uuid=uuid, induk=induk, id_lembaga=id_lembaga,
            id_pendidikan=id_pendidikan, tanggal_masuk=tanggal_masuk)
        if updatePelajar == 200:
            sukses = "Update Nomor Induk Nanda : {} Sukses".format(nama)
            print(sukses)
            logger.info(sukses)
        else:
            gagal = "Update Nomor Induk Nanda : {} Gagal\nSilahkan cek Log".format(nama)
            print(gagal)
            logger.info(gagal)

if __name__ == '__main__':
    print '''1. Ambil Data Dari PEDATREN\n2. Update Nomor Induk'''
    try:
        pilih = input("Silahkan Masukkan Pilihan : ")
        if pilih == 1:
            allData()
        elif pilih == 2:
            updateNomorInduk()
        else:
            print ("Pilihan tidak tersedia")
    except:
        print ("Pakai Digits Mas")
