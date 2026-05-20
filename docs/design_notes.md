# Bölüm 2 - Tasarım Notları (Design Notes)

## TM-1: Unary -> Binary Çevirici
* **1. Strateji:** Makine, unary 1'leri sağa bir `#` işareti ekleyerek sayar. Gördüğü en sağdaki işlenmemiş `1`'i `X` yapar, ardından `#` işaretinin sağındaki ikili sayıyı (Bölüm 1'deki binary increment mantığını kullanarak) bir artırır. Tüm 1'ler bitince yardımcı sembolleri temizler.
* **2. Durum sayısı:** Toplam 8 durum kullandım. Başlangıç, 1 arama, ikili sayıya geçiş, artırma ve temizleme adımları için bu sayının optimum olduğunu düşünüyorum.
* **3. Şerit alfabesi seçimi:** İşlenen 1'leri işaretlemek için `X`, unary ve binary bölümleri birbirinden ayırmak için `#` kullandım.
* **4. Karmaşıklık:** O(N^2). N adet 1 için makine her defasında şeridin bir ucundan diğer ucuna gidip gelmektedir.
* **5. Hata ayıklama hikayesi:** İkili (binary) sayıyı bir artırıp yeni unary 1 bulmak için sola döndüğünde, makine ikili kısımdaki `1` rakamını unary `1` zannedip yanlışlıkla `X` yapıyordu. İkili kısım ile unary kısım birbirine karışmıştı. Çözüm olarak araya `q_return_to_hash` adında yeni bir durum ekledim; böylece makine önce `0` ve `1`'leri atlayıp `#` sembolüne kadar güvenle dönüyor, ondan sonra unary 1 aramaya başlıyor.

## TM-2: İki İkili Sayıyı Karşılaştıran TM
* **1. Strateji:** İki sayıyı en sağdan (LSB) sola doğru karşılaştıran bir "ping-pong" algoritması tasarladım. Önce B sayısının son rakamını işaretleyip hangi rakam olduğunu bir durumda (state) hafızaya alır, sonra A'nın son rakamına gidip ikisini kıyaslar ve kimin büyük olduğunu (tie, A_wins, B_wins) tutarak sola doğru ilerler.
* **2. Durum sayısı:** 22 durum. A ve B'nin o anki güncel şampiyonunu (kimin büyük olduğunu) hafızada tutabilmek için arama durumlarını (seek_A, seek_B) her ihtimal için kopyalamak zorunda kaldım.
* **3. Şerit alfabesi seçimi:** A'nın okunan bitleri için `X`, B'nin okunan bitleri için `Y` kullandım.
* **4. Karmaşıklık:** O(N^2). Her bir bit karşılaştırması için iki sayı arasında sürekli gidip gelinir.
* **5. Hata ayıklama hikayesi:** Farklı uzunluktaki sayıları (örneğin 100 ve 11) kıyaslarken başlarda kafa karışıklığı oldu. B'nin bitleri bittiğinde A'da hala bit kalmışsa makine çöküyordu. B'nin bittiğini `#` okuyarak anladığım an, A'da hala okumadığı bit kalıp kalmadığına bakan `q_check_A` durumunu ekleyip, "daha uzun olan daha büyüktür" mantığını kodlayarak sorunu çözdüm.

## TM-3: Dizgi Kopyalayıcı
* **1. Strateji:** Dizginin sonuna `#` ayıracı koyulur. Baştan başlanarak sırayla `a` karakteri `A`, `b` karakteri `B_` yapılarak işaretlenir. Ardından en sağa gidilip kopyası yazılır, sonra sola (işaretli harfe) geri dönülüp bir sonraki karakter alınır. İşlem bitince büyük harfler tekrar küçültülür.
* **2. Durum sayısı:** 11 durum. İşaretleme, boşluğu bulma, harfi kopyalama, geri dönme ve en sondaki temizleme (unmark) aşamaları için kullandım.
* **3. Şerit alfabesi seçimi:** Kopyalanmış harflerle henüz kopyalanmamışları ayırt etmek için büyük `A` ve `B_` yardımcı sembollerini seçtim.
* **4. Karmaşıklık:** O(N^2). N uzunluğunda dizgi için N kez sona gidip kopyalama işlemi yapar.
* **5. Hata ayıklama hikayesi:** Karakteri en sağa başarıyla yazıyordu ama yeni karakteri okumak için geri dönerken nerede duracağını bilemeyip şeridin en başına kadar gidiyordu. Geri dönerken sadece `a`, `b` ve `#` karakterlerini atlayıp, ilk gördüğü büyük harfte (`A` veya `B_`) durmasını sağlayan `q_return_mark` döngüsünü kurarak bu hedefi bulamama bug'ını hallettim.

## TM-4: 4'e Bölünebilirlik Testi (Student Choice)
* **1. Strateji:** İkili (binary) tabanda bir sayının 4'e bölünebilmesi için son iki rakamının `00` olması yeterlidir (veya sayının kendisi sadece `0` olmalıdır). Makine şeridin en sağına kadar gidip, sondan başlayarak geriye doğru sadece son iki biti kontrol eder.
* **2. Durum sayısı:** Sadece 4 durum yetti. Sona gitmek ve son iki karakteri sırayla kontrol edip durmak makineyi çok küçük ve verimli kıldı.
* **3. Şerit alfabesi seçimi:** Girdi alfabesi `0, 1` haricinde sadece sınır belirten `B` kullanıldı. Yardımcı bir sembole gerek kalmadı.
* **4. Karmaşıklık:** O(N). Makine sadece bir kez baştan sona doğru tarama yapar, hiçbir zaman geriye uzun uzadıya dönmez.
* **5. Hata ayıklama hikayesi:** Kod ilk başta gayet iyi çalışıyordu ama sadece "0" girdisi verildiğinde son iki rakam (ikinci sıfır) var olmadığı için makine sonsuz boşluğa (B) düşüp çöküyordu. İkinci rakamı kontrol eden `q_check2` durumunda `B` (boşluk) gelirse sayının tek başına 0 olduğunu anlayıp onu da "kabul (accept)" etmesi için istisnai bir geçiş kuralı ekledim.
