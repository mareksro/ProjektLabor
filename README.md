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
problemas nostadne seit

<h5>Darba mērķis</h5>
Projekta mērķis - Izstrādāt web lapu kas uzrāda izejošo pasūtījumu informāciju kā laiks un attālums, kur algoritms aprēķina izdevīgāko maršrutu pasūtījuma piegādei.<br>
Algoritma darbības mērķis - Pēc pasūtījumu galamērķiem tiek izveidoti maršruti maksimālajam kurjeru daudzumam, kas mums ir pieejams. Ja visi kurjeri ir aizņemti, algoritms ievāc tekošos datus un nākamajā dienā dod jaunus mašrutus, prioritāri ņemot galamērķus kas ir nākamie rindā. 

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
es nezinu kas tas ir bet lkm vajag

### Algoritms
![Blokshema](https://github.com/user-attachments/assets/d2cb4d61-2b8f-4532-aa40-c99f291101c8)

### Algoritma pseidokods
START
  // User Login or Registration
  INPUT username, password
  IF user_has_account(username, password) THEN
    LOGIN
  ELSE
    REGISTER(username, password)
    LOGIN
  ENDIF
  
  WHILE TRUE DO
    DISPLAY "Select an option:"
    DISPLAY "1 - Create a route"
    DISPLAY "2 - Generate a new route"
    DISPLAY "3 - View existing routes"
    DISPLAY "4 - Exit program"
    INPUT user_choice
    
    IF user_choice == 1 THEN
      // Option 1: Create a Route
      WHILE TRUE DO
        INPUT address
        SAVE_TO_DATABASE(address)
        DISPLAY "Address saved. Do you want to:"
        DISPLAY "1 - Add another address"
        DISPLAY "2 - Go back to main menu"
        INPUT sub_choice
        IF sub_choice == 2 THEN
          BREAK
        ENDIF
      ENDWHILE
      
    ELSE IF user_choice == 2 THEN
      // Option 2: Generate a New Route
      WHILE TRUE DO
        GENERATE_PENDING_ROUTE()
        DISPLAY "Do you want to:"
        DISPLAY "1 - Approve the routes"
        DISPLAY "2 - Generate new routes"
        INPUT sub_choice
        IF sub_choice == 1 THEN
          APPROVE_ROUTES()
          DISPLAY "Do you want to view approved routes?"
          DISPLAY "1 - Yes"
          DISPLAY "2 - No, return to main menu"
          INPUT view_choice
          IF view_choice == 1 THEN
            user_choice = 3 // Redirect to option 3
          ELSE
            BREAK
          ENDIF
        ENDIF
      ENDWHILE
      
    ELSE IF user_choice == 3 THEN
      // Option 3: View Existing Routes
      DISPLAY "How do you want to view routes?"
      DISPLAY "1 - Table"
      DISPLAY "2 - Map"
      INPUT view_choice
      IF view_choice == 1 THEN
        routes = FETCH_APPROVED_ROUTES_FROM_DATABASE()
        DISPLAY_TABLE(routes)
        DISPLAY "Do you want to mark a route as completed?"
        DISPLAY "1 - Yes"
        DISPLAY "2 - No"
        INPUT complete_choice
        IF complete_choice == 1 THEN
          INPUT route_id
          MARK_ROUTE_AS_COMPLETED(route_id)
          DELETE_USED_ADDRESSES(route_id)
        ENDIF
      ELSE IF view_choice == 2 THEN
        routes = FETCH_APPROVED_ROUTES_FROM_DATABASE()
        DISPLAY_MAP(routes)
      ENDIF
      
    ELSE IF user_choice == 4 THEN
      // Option 4: Exit Program
      DISPLAY "Thank you for using the Route Management System. Goodbye!"
      BREAK
    ELSE
      DISPLAY "Invalid choice. Please select a valid option."
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
| 1. | Uzņēmums vēlas nodrošināt ātru piegādi, jo pasūtījumam jānonāk pie klienta savlaicīgi. | Jā| Komentārs|
| 2. | Uzņēmums vēlas nogādāt preci labā stāvoklī, jo jānodrošina klienta uzticamība pakalpojumam. | Nē | Komentārs|
| 3. | Uzņēmums vēlas efektīvākus maršrutus, jo jāpiegādā vairākas preces. | Jā | Komentārs|
| 4. | Uzņēmums vēlas prognozēt pasūtījumu skaitu, jo jāmaksimizē peļņa. | Nē | Komentārs|
| 5. | Uzņēmums vēlas uzticamus darbiniekus, jo jānodrošina augsta līmeņa serviss | Nē | Komentārs|
| 6. | Uzņēmums vēlas izvairīties no pēdējā brīdī atceltiem pasūtījumiem, jo tiek tērēti lieki resursi. | Jā | Komentārs|

### Grupas dalībnieku veikumi
| **Grupas dalībnieks** | **Veikums** |
| ------------- | ------------- |
| Lauma Gailīte | |
| Helēna Anna Bunka | |
| Mareks Rozenblats | |
| Deivs Kevins Gūtmanis | |
| Emīls Laucis | |
