import imaplib
import email
import os

# Konfigurasi
EMAIL = "keyaccount.reg01@sibima.id"
PASSWORD = "Email_3216" # Catatan: Jika ini akun Google/Work, pakai App Password
IMAP_SERVER = "imap.gmail.com" # Ganti jadi imap.outlook.com jika pakai Outlook/Exchange
FOLDER_PO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_po")

def tarik_po_otomatis():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    # Cari email yang belum dibaca (UNSEEN) dengan subjek mengandung "PO"
    status, messages = mail.search(None, '(UNSEEN SUBJECT "PO")')
    
    for num in messages[0].split():
        status, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        for part in msg.walk():
            if part.get_content_maintype() == 'multipart': continue
            if part.get('Content-Disposition') is None: continue
            
            filename = part.get_filename()
            if filename and filename.lower().endswith(".pdf"):
                # Simpan ke folder data_po
                filepath = os.path.join(FOLDER_PO, filename)
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                print(f"Berhasil menarik PO: {filename}")
    
    mail.close()
    mail.logout()

if __name__ == "__main__":
    tarik_po_otomatis()