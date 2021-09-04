from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.image import MIMEImage  #引入圖片
from pathlib import Path    #須從某路徑引入圖片

def main():
    content = MIMEMultipart()  # 建立MIMEMultipart物件
    content["subject"] = "Learn Code With Dennis2"  # 郵件標題
    content["from"] = "dils210293@gmail.com"  # 寄件者
    content["to"] = "dils210293@gmail.com"  # 收件者
    content.attach(MIMEText("Demo python send email2"))  # 郵件文本內容
    imagePath = r'C:\Users\dils2\桌面\dog.PNG'
    content.attach(MIMEImage(Path(imagePath).read_bytes()))  # 郵件圖片內容


    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("dils210293@gmail.com", "oftdzsegwltnjcbt")  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
