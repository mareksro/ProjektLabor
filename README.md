# Projektēšanas laboratorija
<h3>Preču piegādes maršrutēšana</h1>

<h6>
Komanda:<br>
  - Lauma Gailīte<br>
  - Helēna Anna Bunka<br>
  - Deivs Kevins Gūtmanis<br>
  - Emīls Laucis<br>
  - Mareks Rozenblats<br>
</h6>

<h2> Ievads </h2>
<h5>Problēmas nostādne</h5>
Maršruta izveidē ir būtiski, ka kurjers ir spējīgs apmeklēt katru adresi, kas tiek dota viņu darbdienā un ir nepieciešams pēc iespējas efektīvāk piegādāt esošos pasūtījumus.

<h5>Darba mērķis</h5>
Projekta mērķis - Izstrādāt web lapu kas uzrāda kurjeru informāciju - veicamais maršruts un tā laiks, kur algoritms aprēķina izdevīgāko maršrutu pasūtījuma piegādei.<br>
Algoritma darbības mērķis - Pēc pasūtījumu galamērķiem tiek izveidoti maršruti maksimālajam kurjeru daudzumam, kas mums ir pieejams. Ja visi kurjeri ir aizņemti, algoritms ievāc tekošos datus un nākamajā dienā dod jaunus mašrutus. 

<h2>Līdzīgo risinājumu pārskats</h2>
<h5>Līdzīgi tehniskie risinājumi<br>
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
 
<h2>Tehniskais risinājums</h2>

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
![Ekrānuzņēmums 2025-01-12 134026](https://github.com/user-attachments/assets/5f4a7185-1123-42d8-a5fb-bac9b6b92be4)

### Tehnoloģiju steks
Front-end (klienta puses) tehnoloģijas: Javascript, CSS, HTML, Pārlūks <br>
Satvars (servera puse): Flask <br>
Programmēšanas valoda: Python <br>
Datu bāze datu glabāšanai: PostgreSQL <br>
Serveris: Internet Information Services <br>
OS: Windows Server 2022 <br>
Virtualizācija: Oracle VMBox <br> 

### Programmatūras apraksts
Programma tiek rakstīta uz Python valodas, un tā kā mērķis ir izveidot mājaslapu, tiek izmantots Flask mājaslapu aplikācijas ietvars. Python Flask programma ietver vairākas funckijas, lai izstrādātu funkcionējamu maršruta izveidi un atlasi, ļaujot lietotājiem ievadīt konkrētu adresi vai vairākas. Pēc iespējas vairākas adreses tiek izdalītas katram kurjeram, lai kopējais maršruts būtu izdevīgs adrešu apmeklējuma nolūkos un lai iekļautos kurjera darbdienā. Programma ir apvienota ar lietotājiem draudzīgu saskarni, kur pats lietotājs var viegli mijiedarboties ar to. Visi ievadītie maršruti, reģistrētie lietotāji un adreses tiek saglabātas datubāzē ar PostgreSQL palīdzību, kas ir apvienota ar programmu. Pabeigtie maršruti tiek dzēsti, neuzrādot tos vairāk datubāzē.

### Algoritms
![Blokshema](https://github.com/user-attachments/assets/d2cb4d61-2b8f-4532-aa40-c99f291101c8)

### Algoritma pseidokods<br>

START
  // User Ielogoties vai Reģistrēties
  INPUT username, password
  IF user_has_account(username, password) THEN
    LOGIN
  ELSE
    REGISTER(username, password)
    LOGIN
  ENDIF

WHILE TRUE DO
  DISPLAY "1 - Ievadīt adresi"
  DISPLAY "2 - Ģenerēt maršrutu"
  DISPLAY "3 - Maršrutu apstiprināšana"
  DISPLAY "4 - Maršrutu karte"
  DISPLAY "5 - Iziet"
  INPUT user_choice

  IF user_choice == 1 THEN
    // Option 1: Ievadīt adresi
    WHILE TRUE DO
      INPUT address
      SAVE_TO_DATABASE(address)
      DISPLAY "Adrese saglabāta. Vai vēlaties:"
      DISPLAY "1 - Ievadīt vēl vienu adresi"
      DISPLAY "2 - Atgriezties izvēlē"
      INPUT sub_choice
      IF sub_choice == 2 THEN
        BREAK
      ENDIF
    ENDWHILE

  ELSE IF user_choice == 2 THEN
    // Option 2: Ģenerēt maršrutu
    WHILE TRUE DO
      GENERATE_PENDING_ROUTE()
      DISPLAY "Maršruts ģenerēts. Vai vēlaties:"
      DISPLAY "1 - Ģenerēt jaunu maršrutu"
      DISPLAY "2 - Atgriezties izvēlē"
      INPUT sub_choice
      IF sub_choice == 1 THEN
        CONTINUE
      ELSE IF sub_choice == 2 THEN
        BREAK
      ENDIF
    ENDWHILE

  ELSE IF user_choice == 3 THEN
    // Option 3: Maršrutu apstiprināšana
    routes = FETCH_PENDING_ROUTES_FROM_DATABASE()
    DISPLAY "Apstiprināmo maršrutu tabula:"
    DISPLAY_TABLE(routes)
    DISPLAY "1 - Apstiprināt maršrutu"
    DISPLAY "2 - Atzīmēt kā pabeigtu un izdzēst adreses"
    DISPLAY "3 - Atgriezties izvēlē"
    INPUT sub_choice
    IF sub_choice == 1 THEN
      INPUT route_id
      APPROVE_ROUTE(route_id)
    ELSE IF sub_choice == 2 THEN
      INPUT route_id
      MARK_ROUTE_AS_COMPLETED(route_id)
      DELETE_USED_ADDRESSES(route_id)
    ELSE IF sub_choice == 3 THEN
      BREAK
    ENDIF

  ELSE IF user_choice == 4 THEN
    // Option 4: Maršrutu karte
    routes = FETCH_APPROVED_ROUTES_FROM_DATABASE()
    DISPLAY_MAP(routes)
    DISPLAY "1 - Atgriezties izvēlē"
    INPUT sub_choice
    IF sub_choice == 1 THEN
      BREAK
    ENDIF

  ELSE IF user_choice == 5 THEN
    // Option 5: Iziešana no programmas
    DISPLAY "Uz redzēšanos!"
    BREAK

  ELSE
    DISPLAY "Nederīga izvēle. Lūdzu mēģiniet vēlreiz."
  ENDIF
ENDWHILE
END


<h2>Novērtējums</h2>

### Novērtēšanas plāns
<h5>Novērtēšanas mērķis</h5>

### Novērtēšanas rezultāts

<h2>Secinājumi</h2>

### Prasību izpildes kontrolsaraksts
| **Nr** | **Lietotāju stāsts** | **Izpildīts (Jā/Nē)** | **Komentārs** |
| ------------- | ------------- | -------------  | -------------  |
| 1. | Uzņēmums vēlas nodrošināt ātru piegādi, jo pasūtījumam jānonāk pie klienta savlaicīgi. | Jā| Algoritms izveido kurjera maršrutu tā, lai būtu jābrauc pa īsāko ceļu.|
| 2. | Uzņēmums vēlas nogādāt preci labā stāvoklī, jo jānodrošina klienta uzticamība pakalpojumam. | Nē | Šis netika izstrādāts, jo tas nav vērsts uz web lapas izstrādi, bet gan cilvēkresursiem, cik atbildīgi ir kurjeri un noliktavas darbinieki. |
| 3. | Uzņēmums vēlas efektīvākus maršrutus, jo jāpiegādā vairākas preces. | Jā | Izstrādātais algoritms kurjeram izveido maršrutu ar pēc iespējas vairāk gala punktiem balstoties uz to ka kurjeram vidēji darba diena ir 7h 30 min.|
| 4. | Uzņēmums vēlas prognozēt pasūtījumu skaitu, jo jāmaksimizē peļņa. | Nē | Šis netika izstrādāts, jo nepietika laika, taču ja būtu vēl laiks un daudz ievadies dati uz ko balstīties, uzņēmumam tas būtu noderīgi.|
| 5. | Uzņēmums vēlas uzticamus darbiniekus, jo jānodrošina augsta līmeņa serviss | Nē | Šis netika izpildīts jo attiecas uz cilvēkresursiem nevis web lapas izstrādi.|
| 6. | Uzņēmums vēlas izvairīties no pēdējā brīdī atceltiem pasūtījumiem, jo tiek tērēti lieki resursi. | Jā | Ja adrese tiek ievadīta datu bāzē, tad kurjers sūtījumu piegādās klientam, jo ievadot adresi vairs nav iespējams atcelt sūtījumu.|

### Grupas dalībnieku veikumi
| **Grupas dalībnieks** | **Veikums** |
| ------------- | ------------- |
| Lauma Gailīte | Līdzīgo risinajumu pārskats, lietotāju stāsti, konceptu modeļa diagramma, tehnoloģiju steks, UI dizains. |
| Helēna Anna Bunka | Līdzīgo risinajumu pārskats, lietotāju stāsti, konceptu modeļa diagramma, tehnoloģiju steks, back-end, blokshēma, pseidokods, prasību izpildes kontrolsaraksts.|
| Mareks Rozenblats | Līdzīgo risinajumu pārskats, lietotāju stāsti, konceptu modeļa diagramma, tehnoloģiju steks, back-end, datu bāze.|
| Deivs Kevins Gūtmanis | Līdzīgo risinajumu pārskats, lietotāju stāsti, konceptu modeļa diagramma, tehnoloģiju steks, serveris, blokshēma.|
| Emīls Laucis | Līdzīgo risinajumu pārskats, lietotāju stāsti, konceptu modeļa diagramma, datu bāze, daļēji back-end, efektivitāes novērtēšana, plakāts.|
