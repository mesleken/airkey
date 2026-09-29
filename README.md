# AirKey Prototip

Bu proje, "AirKey" kamera tabanlı havada yazma klavyesi için bir Faz 0 prototipidir.

## Kurulum ve Çalıştırma

Gereksinimler zaten sanal ortama (`venv`) yükleniyor. Yükleme tamamlandıktan sonra aşağıdaki komutları kullanarak Faz 0 testini başlatabilirsiniz:

1. Powershell veya Command Prompt açın.
2. Proje dizinine gidin:
```powershell
cd "C:\Users\maozk\Desktop\Virtual Keyboard\airkey"
```
3. Sanal ortamı aktif hale getirin:
```powershell
.\venv\Scripts\Activate.ps1
```
4. Ana betiği çalıştırın:
```powershell
python src\airkey\main.py
```

## Kullanım
- Elinizi kameraya gösterin. İşaret parmağı ucunda bir imleç belirecektir.
- **Tıklama:** Baş parmağınızı işaret parmağınızdan uzaklaştırıp (açıp) tekrar kapatarak "tıklama" yapabilirsiniz. (100ms - 600ms arasında olmalı).
- Tıklama yapıldığında ekranda "CLICK!" yazısı belirecek ve konsola yazdırılacaktır.
- Çıkmak için pencere üzerindeyken **ESC** tuşuna basın.
