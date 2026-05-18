# TuringLab - TM Motoru

Bu proje, Python tabanlı bir Deterministik Tek Şeritli Turing Makinesi (Deterministic Single-Tape Turing Machine) simülatörüdür.
Ödevin Bölüm 1 gereksinimlerine uygun olarak "öğrenci mantığıyla" ve dış bağımlılıklar asgari düzeyde tutularak yazılmıştır. Sadece `PyYAML` gerektirir.

## Özellikler
- Yaml dosyasından makine tanımını yükleme
- Negatif şerit (kafa sola taştığında) desteği
- Adım adım `verbose` çalıştırma ve konfigürasyon geçmişi
- Başarı (accept), Çökme (no_transition), Zaman aşımı (timeout) durumlarını güvenle yakalama

## Kullanım Örneği

Motoru kullanarak bir Turing makinesini kolayca çalıştırabilirsiniz:

```python
from turinglab import SingleTapeTM

# 1. Makineyi Yükle
tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")

# 2. Makineyi Çalıştır (örneğin 1011 stringini vererek)
result = tm.run("1011", max_steps=1000, verbose=True)

# 3. Sonuçları İncele
print("Kabul edildi mi?", result.accepted)
print("Durma Nedeni:", result.reason)
print("Son Şerit:", result.final_tape.strip("B"))
print("Atılan Adım Sayısı:", result.steps)
```

## Sık Sorulan Sorular (Kenar Durumları)
**Kafa sola taşarsa (head_position < 0) ne olur?**
Sonsuz şerit mantığını korumak için, makine sola doğru taştığında şeridin başına (soluna) dinamik olarak yeni bir boş (Blank) karakter eklenir ve kafa konumu sıfırlanarak kesintisiz okuma-yazma yapması sağlanır. Bu yüzden negatif index hatası alınmaz.

## Testleri Çalıştırmak
Projedeki tüm testleri çalıştırmak için `pytest` kullanabilirsiniz:
```bash
pytest tests/
```
