# Projektēšanas laboratorija
<h3>Preču piegādes maršrutēšana</h1>

<h6>
Komanda:<br>
  - Lauma Gailīte<br>
  - Helēna Anna Bunka<br>
  - Kevins Deivs Gūtmanis<br>
  - Emīls Laucis<br>
  - Mareks Rozenblats<br>
</h6>
<h5><b>Risinājumu pārskats</b>
  – Līdzīgi tehniskie risinājumi<br>
    • Atrast un izvērtēt līdzīgos risinājums<br>
    • Aprakstīt līdzīgos risinājumus<br>
    • Apkopot novērojumus tabulā<br>
  – Iepazīties ar intelektisko algoritmu<br>
<br></h5>

| Uzņēmums  | algoritms | Funkcionalitāte | Priekšrocības | Trūkumi |
| ------------- | ------------- | -------------  | -------------  | -------------  |
|Google maps| Dijkstra, VRP | Īsākā maršruta atrašana līdz galamērķim ņemot vērā satiksmi| Ar VRP palīdzību tiek minimizēts veicamo pagriezienu skaits krustojumos | Viedierīču resursu intensīva izmantošana (internets, baterija)|
| Waze  | Dijkstra | Aprēķina īsāko ceļu no lietotāja atrašanās vietas līdz galamērķim | Reāllaika paziņojumi, Alternatīvu maršrutu izvēle | Pārak liela uzticība lietotāju ievadītajiem paziņojumiem|
| Wolt  | GDM (google distance matrix API) | Algoritms ņem vērā ātrāko veidu kā nokļūt līdz izvēlētajam galamērķim ņemot vērā ceļā pavadīto laiku līdz tam no vairākam lokācijām | Efektīva apstrāde izmantojot parallel computing | Izmanto salīdzinoši lielus RAM resursus|
| Routific | Bees Algorithm | Algoritms balstās uz paralēlo algoritma implementāciju (vairākas zonas tiek analizētas vienlaicīgi) | Vienkāršība un smalkas izpētes iespējas savstarpēji līdzīgiem objektiem  | Nav optimāls plašu teritoriju analizēšanai, liela pašizmaksa |
| DHL | Ant Colony Optimization, TSP | Tiek ņemts vērā gan īsākais gan "labākais ceļš", ņemot vērā tikai visvairāk izmantotos maršrutus un reāllaika aktivitāti (piemēram uz ceļa), neizmantojot datus no retāk veiktajiem maršrutiem.| Efektīvs sarežģītu optimizācijas problēmu risināšanā, kā arī dinamiski pielāgojas mainīgiem apstākļiem. | Lēns konverģences ātrums sarežģītos gadījumos un heuristiska metode, kas nenodrošina garantētu optimālu risinājumu. |
| Omniva  | QR, svītru kodi, CTS (Courier tracking systems) | Skeneri nolasa kodus dažādos kontrolpunktos piegādes maršrutā, atjauninot sistēmu ar atrašanās vietas un statusa datiem.| Paziņojumi par pasūtījuma piegadāšanu konrolpunktos / galapunktā | Limitēts informācijas daudzums par pasūtījumu, Nav reāllaika gps izsekošana|

 <h6><em>"Sometimes Google has better traffic data, I assume because they grab location data from every android device, while Waze only uses data from active Waze App users. On routes where many Wazers travel, I find the Waze data to be very percise, ETA times barely differ. Waze foruma ieraksts: https://www.waze.com/forum/viewtopic.php?t=218943"<br>

 <br> "Ant-colony optimization algorithm-based programs have helped companies like DHL identify cost savings in the ground logistic network for supply chain transportation analysts. Publications show that the program has helped the company save millions of dollars annually and increase its profits by more than 15% compared with previous processes." Avots: https://pubsonline.informs.org/doi/abs/10.1287/inte.2020.1046</em></h6>

### Lietotāju stāsti
| **Nr** | **Lietotāju stāsts** | **Prioritāte** |
| ------------- | ------------- | -------------  |
| 1. | Uzņēmums vēlas nodrošināt ātru piegādi, jo pasūtījumam jānonāk pie klienta savlaicīgi. | Zema |
| 2. | Uzņēmums vēlas nogādāt preci labā stāvoklī, jo jānodrošina klienta uzticamība pakalpojumam. | Augsta |
| 3. | Uzņēmums vēlas efektīvākus maršrutus, jo jāpiegādā vairākas preces. | Augsta |
| 4. | Uzņēmums vēlas prognozēt pasūtījumu skaitu, jo jāmaksimizē peļņa. | Vidēja |
| 5. | Uzņēmums vēlas uzticamus darbiniekus, jo jānodrošina augsta līmeņa serviss | Augsta | 
| 6. | Uzņēmums vēlas izvairīties no pēdējā brīdī atceltiem pasūtījumiem, jo tiek tērēti lieki resursi. | Augsta |

### Konceptu modeļu diagramma
<img width="511" alt="Screenshot 2024-11-06 at 11 13 58" src="https://github.com/user-attachments/assets/5022afb9-0fd5-4392-b4e3-0491f3981cb7">

### Tehnoloģiju steks
Front-end (klienta puses) tehnoloģijas: Javascript, CSS, HTML, Pārlūks <br>
Satvars (servera puse): Flask <br>
Programmēšanas valoda: Python <br>
Datu bāze datu glabāšanai: PostgreSQL <br>
Serveris: Apache <br>
OS: Ubuntu Server 24.04LTS<br>
Virtualizācija: Oracle VMBox <br> 

