Version: 4.0.3b. Author of this version: <a href="https://github.com/AndreyKaiu/advanced-browser-mod-kaiu-2026">https://github.com/AndreyKaiu/advanced-browser-mod-kaiu-2026</a><br>
Author of the original addon: <a href="https://github.com/AnKing-VIP">https://github.com/AnKing-VIP</a>
<details>
<summary><b> =EN= Notes. Click to expand</b></summary>
The configuration options are:<br>
<br>
- <b>"Card Info Dialog Always On Top"</b>: Boolean (i.e. "true" or "false"). Allows you to display information about the map in a window that will be on top of the window that called it.<br>
<br>
- <b>"Column alignment"</b>: Either:<br>
&nbsp&nbsp&nbsp- <i><b>"Start"</b></i>: text in column is left aligned (or right aligned for right-to-left scripts)<br>
&nbsp&nbsp&nbsp- <i><b>"Center"</b></i>: text in column is center aligned<br>
<br>
- <b>"Hide custom row highlighting"</b>: Boolean (i.e. "true" or "false"). Removes any row highlighting within the table that was applied by this add-on.<br>
<br>
- <b>"Hide the button for which the value is set to one"</b>: String. To hide all buttons above the table, set this to "1". To hide specific buttons, place a "1" at the corresponding position (counting from the left). For example, "001000000" will hide the third button, while the remaining eight standard buttons will remain visible.<br>
<br>
- <b>"Hide the query string used to generate the table"</b>: Boolean (i.e. "true" or "false"). Hides the text displayed above the table, which serves to clarify the specific query used to retrieve the data.<br>
<br>
- <b>"Language</b>: String. If an empty string is specified, the program will attempt to find a translation file for the language specified by Anki. Otherwise, specify the file name without the extension (for example, "ru" for Russian) located in the add-on's folder (Example location of this file: "...Anki2\addons21\874215009\advancedbrowser\localization\ru.lng" You can open the location of this add-on from the Anki program: Tools -> Add-ons -> Select the name of this add-on -> Click the "View files" button -> Go to the "advancedbrowser\localization" directory). If your language is unavailable, create a copy of the "en.lng" file with a new name (for your language), open the file in a text editor, and translate only the text between the === blocks.<br>
<br>
- <b>"Show internal fields"</b>: Boolean (i.e. "true" or "false"). Enable even more columns that map to database fields related to the cards and notes (dev option).<br>
<br>
- <b>"Show note counts"</b>: Boolean (i.e. "true" or "false"). Show the number of notes (cards and any elements) in the left sidebar.<br>
<br>
- <b>"Table content"</b>: Either:<br>
&nbsp&nbsp&nbsp- <i><b>"No interaction"</b></i>: the table content can't be interacted with. This makes the Advanced Browser behave like the regular Anki browser.<br>
&nbsp&nbsp&nbsp- <i><b>"Selectable"</b></i>: the table content can be selected. All changes will be ignored. This is useful because this allows you to quickly copy field contents (instead of the regular procedure where you have to do all these steps: select the note, move the mouse to the field, select its content, then copy it).<br>
&nbsp&nbsp&nbsp- <i><b>"Editable"</b></i>: Allow to edit some values directly in the table. Not all.<br>
</details>
---
<details>
<summary><b>=RU= Примечания. Клик для открытия</b></summary>
Параметры конфигурации:<br>
<br>
- <b>"Card Info Dialog Always On Top"</b>: Логическое значение (т.е. «true» или «false»). Позволяет отображать информацию о карте в окне, которое будет располагаться поверх окна, вызвавшего эту функцию.<br>
<br>
- <b>"Column alignment"</b>: Одно из:<br>
&nbsp&nbsp&nbsp- <i><b>"Start"</b></i>: текст в столбце выравнивается по левому краю (или по правому — для письма справа налево)<br>
&nbsp&nbsp&nbsp- <i><b>"Center"</b></i>: текст в столбце выравнивается по центру<br>
<br>
- <b>"Hide custom row highlighting"</b>: Логическое значение ("true" или "false"). Убирает подсветку в таблице устанавливаемую этим аддоном.<br>
<br>
- <b>"Hide the button for which the value is set to one"</b>: Строка. Если необходимо скрыть все кнопки над таблицей, то установите "1". Если необходимо скрыть конкретную кнопку, то просто установите символ 1 в нужной позиции кнопки считая слева. Допустим "001000000" — скроет только 3 кнопку и будут показаны только 8 стандартных кнопок.<br>
<br>
- <b>"Hide the query string used to generate the table"</b>: Логическое значение ("true" или "false"). Убирает текстовую строку над таблицей служащую только для уточнения по какому запросу до этого была произведена выборка данных.<br>
<br>
- <b>"Language"</b>: Строка. Если указана пустая строка, программа попытается найти файл перевода для языка, выбранного в Anki. В противном случае укажите имя файла без расширения (например, "ru" для русского), расположенного в папке дополнения (Пример расположения этого файла: "...Anki2\addons21\874215009\advancedbrowser\localization\ru.lng" Вы можете открыть расположение этого дополнения в программе Anki: Инструменты -> Дополнения -> Выберите название этого дополнения -> Нажмите кнопку "Просмотреть файлы" -> Перейдите в каталог "advancedbrowser\localization"). Если вашего языка нет, создайте копию файла <i><b>"en.lng"</b></i> с новым именем (для вашего языка), откройте его в текстовом редакторе и переведите только текст между блоками "===".<br>
<br>
- <b>"Show internal fields"</b>: Логическое значение ("true" или "false"). Включает дополнительные столбцы, соответствующие внутренним полям базы данных, связанным с карточками и записями (опция для разработчиков).<br>
<br>
- <b>"Show note counts"</b>: Логическое значение ("true" или "false"). В левой боковой панели отобразится количество заметок (карточек и любых других элементов).<br>
<br>
- <b>"Table content"</b>: Одно из:<br>
&nbsp&nbsp&nbsp- <i><b>"No interaction"</b></i>: содержимое таблицы недоступно для взаимодействия. Advanced Browser работает как обычный браузер Anki.<br>
&nbsp&nbsp&nbsp- <i><b>"Selectable"</b></i>: содержимое таблицы можно выделять. Все изменения будут проигнорированы. Удобно для быстрого копирования содержимого полей (вместо обычной процедуры: выбрать запись, перейти к полю, выделить содержимое, скопировать).<br>
&nbsp&nbsp&nbsp- <i><b>"Editable"</b></i>: позволяет редактировать некоторые значения прямо в таблице. Не все.<br>
</details>
---
<details>
<summary><b>=AR= ملاحظات. انقر للتوسيع</b></summary>
خيارات التكوين هي:<br>
<br>
- <b>"Card Info Dialog Always On Top"</b>: قيمة منطقية (أي "true" أو "false"). تتيح عرض معلومات البطاقة في نافذة تظهر دائمًا فوق النافذة التي فتحتها.<br>
<br>
- <b>"Column alignment"</b>: أحد الخيارين التاليين:<br>
&nbsp&nbsp&nbsp- <i><b>"Start"</b></i>: تتم محاذاة النص في العمود إلى اليسار (أو إلى اليمين في اللغات التي تُكتب من اليمين إلى اليسار).<br>
&nbsp&nbsp&nbsp- <i><b>"Center"</b></i>: تتم محاذاة النص في العمود إلى الوسط.<br>
<br>
- <b>"Hide custom row highlighting"</b>: قيمة منطقية (أي "true" أو "false"). تزيل أي تمييز للصفوف داخل الجدول تم تطبيقه بواسطة هذه الإضافة.<br>
<br>
- <b>"Hide the button for which the value is set to one"</b>: سلسلة نصية. لإخفاء جميع الأزرار الموجودة فوق الجدول، اضبط القيمة على "1". لإخفاء أزرار محددة، ضع الرقم "1" في الموضع المقابل للزر (بدءًا من اليسار). على سبيل المثال، ستؤدي القيمة "001000000" إلى إخفاء الزر الثالث، مع إبقاء الأزرار القياسية الثمانية الأخرى ظاهرة.<br>
<br>
- <b>"Hide the query string used to generate the table"</b>: قيمة منطقية (أي "true" أو "false"). تخفي النص المعروض فوق الجدول، والذي يوضح الاستعلام المحدد المستخدم لاسترجاع البيانات.<br>
<br>
- <b>"Language"</b>: سلسلة نصية. إذا تم تحديد سلسلة فارغة، فسيحاول البرنامج العثور على ملف ترجمة للغة المحددة في Anki. وإلا، فحدد اسم الملف بدون الامتداد (على سبيل المثال، "ru" للغة الروسية) والموجود في مجلد الإضافة (مثال على موقع هذا الملف: "...Anki2\addons21\874215009\advancedbrowser\localization\ru.lng"). يمكنك فتح مجلد الإضافة من برنامج Anki: الأدوات -> الإضافات -> حدد اسم هذه الإضافة -> انقر على زر "عرض الملفات" -> انتقل إلى مجلد "advancedbrowser\localization"). إذا كانت لغتك غير متوفرة، فأنشئ نسخة من الملف "en.lng" باسم جديد (خاص بلغتك)، وافتحه في محرر نصوص، وترجم النص الموجود فقط بين الكتل ===.<br>
<br>
- <b>"Show internal fields"</b>: قيمة منطقية (أي "true" أو "false"). تتيح عرض المزيد من الأعمدة المرتبطة بالحقول الداخلية لقاعدة البيانات الخاصة بالبطاقات والملاحظات (خيار للمطورين).<br>
<br>
- <b>"Show note counts"</b>: قيمة منطقية (أي "true" أو "false"). تعرض عدد الملاحظات (البطاقات وأي عناصر أخرى) في الشريط الجانبي الأيسر.<br>
<br>
- <b>"Table content"</b>: أحد الخيارات التالية:<br>
&nbsp&nbsp&nbsp- <i><b>"No interaction"</b></i>: لا يمكن التفاعل مع محتوى الجدول. وهذا يجعل Advanced Browser يعمل مثل متصفح Anki العادي.<br>
&nbsp&nbsp&nbsp- <i><b>"Selectable"</b></i>: يمكن تحديد محتوى الجدول. سيتم تجاهل جميع التغييرات. هذا مفيد لأنه يتيح لك نسخ محتويات الحقول بسرعة (بدلاً من الطريقة المعتادة التي تتطلب تحديد الملاحظة، وتحريك الماوس إلى الحقل، وتحديد محتواه، ثم نسخه).<br>
&nbsp&nbsp&nbsp- <i><b>"Editable"</b></i>: يسمح بتعديل بعض القيم مباشرةً في الجدول، ولكن ليس جميعها.<br>
</details>
---
<details>
<summary><b>=ES= Notas. Haz clic para expandir</b></summary>
Las opciones de configuración son:<br>
<br>
- <b>"Card Info Dialog Always On Top"</b>: Valor booleano (es decir, "true" o "false"). Permite mostrar información sobre la tarjeta en una ventana que permanecerá siempre por encima de la ventana que la abrió.<br>
<br>
- <b>"Column alignment"</b>: Una de las siguientes opciones:<br>
&nbsp&nbsp&nbsp- <i><b>"Start"</b></i>: el texto de la columna se alinea a la izquierda (o a la derecha en los idiomas que se escriben de derecha a izquierda).<br>
&nbsp&nbsp&nbsp- <i><b>"Center"</b></i>: el texto de la columna se alinea en el centro.<br>
<br>
- <b>"Hide custom row highlighting"</b>: Valor booleano (es decir, "true" o "false"). Elimina cualquier resaltado de filas dentro de la tabla aplicado por este complemento.<br>
<br>
- <b>"Hide the button for which the value is set to one"</b>: Cadena de texto. Para ocultar todos los botones situados encima de la tabla, establece el valor en "1". Para ocultar botones específicos, coloca un "1" en la posición correspondiente (contando desde la izquierda). Por ejemplo, "001000000" ocultará el tercer botón, mientras que los otros ocho botones estándar permanecerán visibles.<br>
<br>
- <b>"Hide the query string used to generate the table"</b>: Valor booleano (es decir, "true" o "false"). Oculta el texto que aparece encima de la tabla y que indica la consulta específica utilizada para obtener los datos.<br>
<br>
- <b>"Language"</b>: Cadena de texto. Si se especifica una cadena vacía, el programa intentará encontrar un archivo de traducción para el idioma configurado en Anki. De lo contrario, especifica el nombre del archivo sin extensión (por ejemplo, "ru" para ruso), ubicado en la carpeta del complemento (Ejemplo de ubicación: "...Anki2\addons21\874215009\advancedbrowser\localization\ru.lng"). Puedes abrir la carpeta del complemento desde Anki: Herramientas -> Complementos -> Selecciona el nombre de este complemento -> Haz clic en el botón "Ver archivos" -> Ve al directorio "advancedbrowser\localization"). Si tu idioma no está disponible, crea una copia del archivo "en.lng" con un nombre nuevo (correspondiente a tu idioma), ábrelo en un editor de texto y traduce únicamente el texto situado entre los bloques ===.<br>
<br>
- <b>"Show internal fields"</b>: Valor booleano (es decir, "true" o "false"). Activa columnas adicionales correspondientes a los campos internos de la base de datos relacionados con las tarjetas y las notas (opción para desarrolladores).<br>
<br>
- <b>"Show note counts"</b>: Valor booleano (es decir, "true" o "false"). Muestra el número de notas (tarjetas y otros elementos) en la barra lateral izquierda.<br>
<br>
- <b>"Table content"</b>: Una de las siguientes opciones:<br>
&nbsp&nbsp&nbsp- <i><b>"No interaction"</b></i>: no se puede interactuar con el contenido de la tabla. Esto hace que Advanced Browser funcione como el navegador estándar de Anki.<br>
&nbsp&nbsp&nbsp- <i><b>"Selectable"</b></i>: se puede seleccionar el contenido de la tabla. Todos los cambios serán ignorados. Esto resulta útil porque permite copiar rápidamente el contenido de los campos (en lugar del procedimiento habitual, que consiste en seleccionar la nota, mover el ratón hasta el campo, seleccionar su contenido y después copiarlo).<br>
&nbsp&nbsp&nbsp- <i><b>"Editable"</b></i>: permite editar algunos valores directamente en la tabla. No todos.<br>
</details>
---
<details>
<summary><b>=FR= Remarques. Cliquez pour développer</b></summary>
Les options de configuration sont les suivantes :<br>
<br>
- <b>"Card Info Dialog Always On Top"</b> : Valeur booléenne (c'est-à-dire "true" ou "false"). Permet d'afficher les informations de la carte dans une fenêtre qui restera toujours au-dessus de la fenêtre depuis laquelle elle a été ouverte.<br>
<br>
- <b>"Column alignment"</b> : L'une des options suivantes :<br>
&nbsp&nbsp&nbsp- <i><b>"Start"</b></i> : le texte de la colonne est aligné à gauche (ou à droite pour les langues écrites de droite à gauche).<br>
&nbsp&nbsp&nbsp- <i><b>"Center"</b></i> : le texte de la colonne est centré.<br>
<br>
- <b>"Hide custom row highlighting"</b> : Valeur booléenne (c'est-à-dire "true" ou "false"). Supprime toute mise en surbrillance des lignes du tableau appliquée par cette extension.<br>
<br>
- <b>"Hide the button for which the value is set to one"</b> : Chaîne de caractères. Pour masquer tous les boutons situés au-dessus du tableau, définissez cette valeur sur "1". Pour masquer des boutons spécifiques, placez un "1" à la position correspondante (en comptant depuis la gauche). Par exemple, "001000000" masquera le troisième bouton, tandis que les huit autres boutons standard resteront visibles.<br>
<br>
- <b>"Hide the query string used to generate the table"</b> : Valeur booléenne (c'est-à-dire "true" ou "false"). Masque le texte affiché au-dessus du tableau, qui indique la requête spécifique utilisée pour récupérer les données.<br>
<br>
- <b>"Language"</b> : Chaîne de caractères. Si une chaîne vide est spécifiée, le programme essaiera de trouver un fichier de traduction correspondant à la langue définie dans Anki. Sinon, indiquez le nom du fichier sans extension (par exemple, "ru" pour le russe), situé dans le dossier de l'extension (Exemple d'emplacement : "...Anki2\addons21\874215009\advancedbrowser\localization\ru.lng"). Vous pouvez ouvrir le dossier de cette extension depuis Anki : Outils -> Extensions -> Sélectionnez le nom de cette extension -> Cliquez sur le bouton "Afficher les fichiers" -> Accédez au répertoire "advancedbrowser\localization"). Si votre langue n'est pas disponible, créez une copie du fichier "en.lng" avec un nouveau nom (correspondant à votre langue), ouvrez-la dans un éditeur de texte et traduisez uniquement le texte situé entre les blocs ===.<br>
<br>
- <b>"Show internal fields"</b> : Valeur booléenne (c'est-à-dire "true" ou "false"). Active des colonnes supplémentaires correspondant aux champs internes de la base de données liés aux cartes et aux notes (option destinée aux développeurs).<br>
<br>
- <b>"Show note counts"</b> : Valeur booléenne (c'est-à-dire "true" ou "false"). Affiche le nombre de notes (cartes et autres éléments) dans la barre latérale gauche.<br>
<br>
- <b>"Table content"</b> : L'une des options suivantes :<br>
&nbsp&nbsp&nbsp- <i><b>"No interaction"</b></i> : le contenu du tableau ne peut pas être manipulé. Advanced Browser fonctionne ainsi comme le navigateur Anki classique.<br>
&nbsp&nbsp&nbsp- <i><b>"Selectable"</b></i> : le contenu du tableau peut être sélectionné. Toutes les modifications seront ignorées. Cette option est pratique, car elle permet de copier rapidement le contenu des champs (au lieu de suivre la procédure habituelle : sélectionner la note, déplacer la souris vers le champ, sélectionner son contenu, puis le copier).<br>
&nbsp&nbsp&nbsp- <i><b>"Editable"</b></i> : permet de modifier certaines valeurs directement dans le tableau, mais pas toutes.<br>
</details>
---
<details>
<summary><b>=IT= Note. Clicca per espandere</b></summary>
Le opzioni di configurazione sono le seguenti:<br>
<br>
- <b>"Card Info Dialog Always On Top"</b>: Valore booleano (ovvero "true" o "false"). Consente di visualizzare le informazioni sulla scheda in una finestra che rimarrà sempre in primo piano rispetto alla finestra da cui è stata aperta.<br>
<br>
- <b>"Column alignment"</b>: Una delle seguenti opzioni:<br>
&nbsp&nbsp&nbsp- <i><b>"Start"</b></i>: il testo nella colonna è allineato a sinistra (o a destra per le lingue scritte da destra a sinistra).<br>
&nbsp&nbsp&nbsp- <i><b>"Center"</b></i>: il testo nella colonna è centrato.<br>
<br>
- <b>"Hide custom row highlighting"</b>: Valore booleano (ovvero "true" o "false"). Rimuove qualsiasi evidenziazione delle righe della tabella applicata da questo componente aggiuntivo.<br>
<br>
- <b>"Hide the button for which the value is set to one"</b>: Stringa di testo. Per nascondere tutti i pulsanti sopra la tabella, imposta il valore su "1". Per nascondere pulsanti specifici, inserisci un "1" nella posizione corrispondente (contando da sinistra). Ad esempio, "001000000" nasconderà il terzo pulsante, mentre gli altri otto pulsanti standard rimarranno visibili.<br>
<br>
- <b>"Hide the query string used to generate the table"</b>: Valore booleano (ovvero "true" o "false"). Nasconde il testo visualizzato sopra la tabella, che indica la query specifica utilizzata per recuperare i dati.<br>
<br>
- <b>"Language"</b>: Stringa di testo. Se viene specificata una stringa vuota, il programma tenterà di trovare un file di traduzione per la lingua impostata in Anki. Altrimenti, specifica il nome del file senza estensione (ad esempio, "ru" per il russo), situato nella cartella del componente aggiuntivo (Esempio di percorso: "...Anki2\addons21\874215009\advancedbrowser\localization\ru.lng"). Puoi aprire la cartella del componente aggiuntivo da Anki: Strumenti -> Componenti aggiuntivi -> Seleziona il nome di questo componente aggiuntivo -> Fai clic sul pulsante "Visualizza file" -> Vai alla directory "advancedbrowser\localization"). Se la tua lingua non è disponibile, crea una copia del file "en.lng" con un nuovo nome (corrispondente alla tua lingua), aprila in un editor di testo e traduci solo il testo compreso tra i blocchi ===.<br>
<br>
- <b>"Show internal fields"</b>: Valore booleano (ovvero "true" o "false"). Attiva ulteriori colonne corrispondenti ai campi interni del database relativi alle schede e alle note (opzione per sviluppatori).<br>
<br>
- <b>"Show note counts"</b>: Valore booleano (ovvero "true" o "false"). Mostra il numero di note (schede e altri elementi) nella barra laterale sinistra.<br>
<br>
- <b>"Table content"</b>: Una delle seguenti opzioni:<br>
&nbsp&nbsp&nbsp- <i><b>"No interaction"</b></i>: non è possibile interagire con il contenuto della tabella. In questo modo Advanced Browser funziona come il normale browser di Anki.<br>
&nbsp&nbsp&nbsp- <i><b>"Selectable"</b></i>: è possibile selezionare il contenuto della tabella. Tutte le modifiche verranno ignorate. Questa opzione è utile perché consente di copiare rapidamente il contenuto dei campi (invece di seguire la procedura abituale: selezionare la nota, spostare il mouse sul campo, selezionarne il contenuto e poi copiarlo).<br>
&nbsp&nbsp&nbsp- <i><b>"Editable"</b></i>: consente di modificare alcuni valori direttamente nella tabella, ma non tutti.<br>
</details>
---
<details>
<summary><b>=KO= 참고 사항. 클릭하여 펼치기</b></summary>
설정 옵션은 다음과 같습니다.<br>
<br>
- <b>"Card Info Dialog Always On Top"</b>: 불리언 값(즉, "true" 또는 "false")입니다. 카드를 호출한 창보다 항상 위에 표시되는 별도의 창에 카드 정보를 표시할 수 있습니다.<br>
<br>
- <b>"Column alignment"</b>: 다음 중 하나를 선택합니다.<br>
&nbsp&nbsp&nbsp- <i><b>"Start"</b></i>: 열의 텍스트를 왼쪽에 정렬합니다(오른쪽에서 왼쪽으로 쓰는 언어에서는 오른쪽 정렬).<br>
&nbsp&nbsp&nbsp- <i><b>"Center"</b></i>: 열의 텍스트를 가운데에 정렬합니다.<br>
<br>
- <b>"Hide custom row highlighting"</b>: 불리언 값(즉, "true" 또는 "false")입니다. 이 애드온이 테이블에 적용한 모든 행 강조 표시를 제거합니다.<br>
<br>
- <b>"Hide the button for which the value is set to one"</b>: 문자열입니다. 테이블 위에 있는 모든 버튼을 숨기려면 값을 "1"로 설정합니다. 특정 버튼만 숨기려면 해당 버튼의 위치(왼쪽부터 계산)에 "1"을 입력합니다. 예를 들어 "001000000"은 세 번째 버튼을 숨기고 나머지 8개의 기본 버튼은 계속 표시합니다.<br>
<br>
- <b>"Hide the query string used to generate the table"</b>: 불리언 값(즉, "true" 또는 "false")입니다. 데이터를 가져오는 데 사용된 구체적인 검색 조건을 설명하는 테이블 위의 텍스트를 숨깁니다.<br>
<br>
- <b>"Language"</b>: 문자열입니다. 빈 문자열을 지정하면 프로그램은 Anki에서 설정한 언어에 해당하는 번역 파일을 찾으려고 시도합니다. 그렇지 않으면 애드온 폴더에 있는 파일의 확장자를 제외한 이름을 지정합니다(예: 러시아어의 경우 "ru"). 파일 위치 예시: "...Anki2\addons21\874215009\advancedbrowser\localization\ru.lng". Anki 프로그램에서 애드온 폴더를 열 수 있습니다: 도구 -> 애드온 -> 이 애드온 선택 -> "파일 보기" 버튼 클릭 -> "advancedbrowser\localization" 디렉터리로 이동합니다. 해당 언어가 없는 경우 "en.lng" 파일을 복사하여 해당 언어의 새 이름으로 저장한 다음 텍스트 편집기로 열고 === 블록 사이의 텍스트만 번역합니다.<br>
<br>
- <b>"Show internal fields"</b>: 불리언 값(즉, "true" 또는 "false")입니다. 카드 및 노트와 관련된 데이터베이스 내부 필드에 해당하는 추가 열을 표시합니다(개발자용 옵션).<br>
<br>
- <b>"Show note counts"</b>: 불리언 값(즉, "true" 또는 "false")입니다. 왼쪽 사이드바에 노트(카드 및 기타 항목)의 개수를 표시합니다.<br>
<br>
- <b>"Table content"</b>: 다음 중 하나를 선택합니다.<br>
&nbsp&nbsp&nbsp- <i><b>"No interaction"</b></i>: 테이블 내용을 선택하거나 조작할 수 없습니다. Advanced Browser가 일반 Anki 브라우저처럼 작동합니다.<br>
&nbsp&nbsp&nbsp- <i><b>"Selectable"</b></i>: 테이블 내용을 선택할 수 있지만 모든 변경 사항은 무시됩니다. 이 옵션을 사용하면 노트를 선택하고, 필드로 마우스를 이동하고, 내용을 선택한 다음 복사하는 일반적인 절차 없이 필드 내용을 빠르게 복사할 수 있습니다.<br>
&nbsp&nbsp&nbsp- <i><b>"Editable"</b></i>: 일부 값을 테이블에서 직접 수정할 수 있습니다. 모든 값을 수정할 수 있는 것은 아닙니다.<br>
</details>
---
<details>
<summary><b>=HI= नोट्स। विस्तार करने के लिए क्लिक करें</b></summary>
कॉन्फ़िगरेशन विकल्प निम्नलिखित हैं:<br>
<br>
- <b>"Card Info Dialog Always On Top"</b>: बूलियन मान (अर्थात "true" या "false")। यह कार्ड की जानकारी को एक ऐसी विंडो में प्रदर्शित करने की अनुमति देता है जो उसे खोलने वाली विंडो के ऊपर हमेशा दिखाई देगी।<br>
<br>
- <b>"Column alignment"</b>: निम्नलिखित में से एक विकल्प:<br>
&nbsp&nbsp&nbsp- <i><b>"Start"</b></i>: कॉलम में टेक्स्ट बाईं ओर संरेखित होता है (या दाईं ओर, यदि भाषा दाएँ से बाएँ लिखी जाती है)।<br>
&nbsp&nbsp&nbsp- <i><b>"Center"</b></i>: कॉलम में टेक्स्ट बीच में संरेखित होता है।<br>
<br>
- <b>"Hide custom row highlighting"</b>: बूलियन मान (अर्थात "true" या "false")। यह तालिका में इस ऐड-ऑन द्वारा लागू की गई पंक्तियों की सभी हाइलाइटिंग हटा देता है।<br>
<br>
- <b>"Hide the button for which the value is set to one"</b>: टेक्स्ट स्ट्रिंग। तालिका के ऊपर मौजूद सभी बटन छिपाने के लिए इसका मान "1" रखें। केवल कुछ विशेष बटन छिपाने के लिए, बाएँ से गिनते हुए संबंधित स्थान पर "1" रखें। उदाहरण के लिए, "001000000" तीसरे बटन को छिपा देगा, जबकि बाकी आठ मानक बटन दिखाई देते रहेंगे।<br>
<br>
- <b>"Hide the query string used to generate the table"</b>: बूलियन मान (अर्थात "true" या "false")। यह तालिका के ऊपर दिखने वाले उस टेक्स्ट को छिपा देता है जो डेटा प्राप्त करने के लिए उपयोग की गई विशिष्ट क्वेरी बताता है।<br>
<br>
- <b>"Language"</b>: टेक्स्ट स्ट्रिंग। यदि खाली स्ट्रिंग दी जाती है, तो प्रोग्राम Anki में निर्धारित भाषा के लिए अनुवाद फ़ाइल खोजने का प्रयास करेगा। अन्यथा, ऐड-ऑन के फ़ोल्डर में मौजूद फ़ाइल का नाम बिना एक्सटेंशन के निर्दिष्ट करें (उदाहरण के लिए, रूसी भाषा के लिए "ru")। फ़ाइल का उदाहरण स्थान: "...Anki2\addons21\874215009\advancedbrowser\localization\ru.lng"। आप Anki प्रोग्राम से इस ऐड-ऑन का फ़ोल्डर खोल सकते हैं: Tools -> Add-ons -> इस ऐड-ऑन का नाम चुनें -> "View files" बटन पर क्लिक करें -> "advancedbrowser\localization" डायरेक्टरी खोलें। यदि आपकी भाषा उपलब्ध नहीं है, तो "en.lng" फ़ाइल की एक कॉपी अपनी भाषा के नए नाम से बनाएँ, उसे टेक्स्ट एडिटर में खोलें और केवल === ब्लॉकों के बीच के टेक्स्ट का अनुवाद करें।<br>
<br>
- <b>"Show internal fields"</b>: बूलियन मान (अर्थात "true" या "false")। कार्ड और नोट्स से संबंधित डेटाबेस के आंतरिक फ़ील्ड से जुड़े अतिरिक्त कॉलम सक्षम करता है (डेवलपर विकल्प)।<br>
<br>
- <b>"Show note counts"</b>: बूलियन मान (अर्थात "true" या "false")। बाएँ साइडबार में नोट्स (कार्ड और अन्य सभी तत्वों) की संख्या दिखाता है।<br>
<br>
- <b>"Table content"</b>: निम्नलिखित में से एक विकल्प:<br>
&nbsp&nbsp&nbsp- <i><b>"No interaction"</b></i>: तालिका की सामग्री के साथ कोई क्रिया नहीं की जा सकती। इससे Advanced Browser सामान्य Anki ब्राउज़र की तरह काम करता है।<br>
&nbsp&nbsp&nbsp- <i><b>"Selectable"</b></i>: तालिका की सामग्री को चुना जा सकता है। सभी बदलाव अनदेखे कर दिए जाएँगे। यह उपयोगी है क्योंकि इससे फ़ील्ड की सामग्री जल्दी कॉपी की जा सकती है (सामान्य प्रक्रिया में नोट चुनना, माउस को फ़ील्ड तक ले जाना, उसकी सामग्री चुनना और फिर कॉपी करना पड़ता है)।<br>
&nbsp&nbsp&nbsp- <i><b>"Editable"</b></i>: तालिका में कुछ मानों को सीधे संपादित करने की अनुमति देता है। सभी मानों को नहीं।<br>
</details>
---
<details>
<summary><b>=DE= Hinweise. Zum Erweitern anklicken</b></summary>
Die Konfigurationsoptionen sind:<br>
<br>
- <b>"Card Info Dialog Always On Top"</b>: Boolescher Wert (also "true" oder "false"). Ermöglicht es, Informationen zur Karte in einem Fenster anzuzeigen, das immer über dem Fenster liegt, von dem aus es geöffnet wurde.<br>
<br>
- <b>"Column alignment"</b>: Eine der folgenden Optionen:<br>
&nbsp&nbsp&nbsp- <i><b>"Start"</b></i>: Der Text in der Spalte wird linksbündig ausgerichtet (bei Sprachen mit Schreibrichtung von rechts nach links rechtsbündig).<br>
&nbsp&nbsp&nbsp- <i><b>"Center"</b></i>: Der Text in der Spalte wird zentriert ausgerichtet.<br>
<br>
- <b>"Hide custom row highlighting"</b>: Boolescher Wert (also "true" oder "false"). Entfernt alle Zeilenhervorhebungen innerhalb der Tabelle, die von diesem Add-on angewendet wurden.<br>
<br>
- <b>"Hide the button for which the value is set to one"</b>: Zeichenfolge. Um alle Schaltflächen oberhalb der Tabelle auszublenden, setze diesen Wert auf "1". Um bestimmte Schaltflächen auszublenden, setze an der entsprechenden Position (von links gezählt) eine "1". Beispielsweise blendet "001000000" die dritte Schaltfläche aus, während die übrigen acht Standardschaltflächen sichtbar bleiben.<br>
<br>
- <b>"Hide the query string used to generate the table"</b>: Boolescher Wert (also "true" oder "false"). Blendet den oberhalb der Tabelle angezeigten Text aus, der die konkrete Abfrage zur Abfrage der Daten beschreibt.<br>
<br>
- <b>"Language"</b>: Zeichenfolge. Wenn eine leere Zeichenfolge angegeben wird, versucht das Programm, eine Übersetzungsdatei für die in Anki eingestellte Sprache zu finden. Andernfalls gib den Dateinamen ohne Erweiterung an (z. B. "ru" für Russisch). Die Datei befindet sich im Add-on-Ordner (Beispielpfad: "...Anki2\addons21\874215009\advancedbrowser\localization\ru.lng"). Du kannst den Ordner des Add-ons direkt in Anki öffnen: Werkzeuge -> Add-ons -> Dieses Add-on auswählen -> Auf die Schaltfläche "Dateien anzeigen" klicken -> Zum Verzeichnis "advancedbrowser\localization" wechseln. Wenn deine Sprache nicht verfügbar ist, erstelle eine Kopie der Datei "en.lng" mit einem neuen Namen für deine Sprache, öffne sie in einem Texteditor und übersetze nur den Text zwischen den ===-Blöcken.<br>
<br>
- <b>"Show internal fields"</b>: Boolescher Wert (also "true" oder "false"). Aktiviert zusätzliche Spalten, die den internen Datenbankfeldern zu Karten und Notizen entsprechen (Entwickleroption).<br>
<br>
- <b>"Show note counts"</b>: Boolescher Wert (also "true" oder "false"). Zeigt die Anzahl der Notizen (Karten und andere Elemente) in der linken Seitenleiste an.<br>
<br>
- <b>"Table content"</b>: Eine der folgenden Optionen:<br>
&nbsp&nbsp&nbsp- <i><b>"No interaction"</b></i>: Der Tabelleninhalt kann nicht bearbeitet oder ausgewählt werden. Dadurch verhält sich Advanced Browser wie der normale Anki-Browser.<br>
&nbsp&nbsp&nbsp- <i><b>"Selectable"</b></i>: Der Tabelleninhalt kann ausgewählt werden. Alle Änderungen werden ignoriert. Dies ist praktisch, da sich Feldinhalte schnell kopieren lassen (anstatt des üblichen Vorgehens: Notiz auswählen, mit der Maus zum Feld wechseln, dessen Inhalt markieren und anschließend kopieren).<br>
&nbsp&nbsp&nbsp- <i><b>"Editable"</b></i>: Ermöglicht es, einige Werte direkt in der Tabelle zu bearbeiten. Nicht alle Werte sind bearbeitbar.<br>
</details>
---
<details>
<summary><b>=JA= 注意事項。クリックして展開</b></summary>
設定オプションは次のとおりです。<br>
<br>
- <b>"Card Info Dialog Always On Top"</b>: 真偽値（"true" または "false"）。カード情報を、呼び出し元のウィンドウより常に手前に表示される別のウィンドウに表示できます。<br>
<br>
- <b>"Column alignment"</b>: 次のいずれかを指定します。<br>
&nbsp&nbsp&nbsp- <i><b>"Start"</b></i>: 列内のテキストを左揃えにします（右から左に書く言語では右揃えになります）。<br>
&nbsp&nbsp&nbsp- <i><b>"Center"</b></i>: 列内のテキストを中央揃えにします。<br>
<br>
- <b>"Hide custom row highlighting"</b>: 真偽値（"true" または "false"）。このアドオンによってテーブル内の行に適用された強調表示をすべて解除します。<br>
<br>
- <b>"Hide the button for which the value is set to one"</b>: 文字列。テーブル上部のすべてのボタンを非表示にするには、値を "1" に設定します。特定のボタンだけを非表示にするには、左から数えた対応する位置に "1" を指定します。たとえば、"001000000" と設定すると3番目のボタンだけが非表示になり、残りの8個の標準ボタンは表示されたままになります。<br>
<br>
- <b>"Hide the query string used to generate the table"</b>: 真偽値（"true" または "false"）。テーブルの上に表示される、データ取得に使用された具体的な検索条件を示すテキストを非表示にします。<br>
<br>
- <b>"Language"</b>: 文字列。空の文字列を指定すると、プログラムはAnkiで設定されている言語に対応する翻訳ファイルを検索します。それ以外の場合は、アドオンのフォルダー内にあるファイル名を拡張子なしで指定します（例：ロシア語の場合は "ru"）。ファイルの場所の例："...Anki2\addons21\874215009\advancedbrowser\localization\ru.lng"。Ankiからアドオンのフォルダーを開くには、ツール -> アドオン -> このアドオンを選択 -> 「ファイルを表示」ボタンをクリック -> "advancedbrowser\localization" ディレクトリを開きます。使用したい言語がない場合は、"en.lng" ファイルをコピーして、その言語用の新しい名前で保存します。テキストエディターで開き、=== ブロックの間にあるテキストだけを翻訳してください。<br>
<br>
- <b>"Show internal fields"</b>: 真偽値（"true" または "false"）。カードとノートに関連するデータベースの内部フィールドに対応する追加の列を表示します（開発者向けオプション）。<br>
<br>
- <b>"Show note counts"</b>: 真偽値（"true" または "false"）。左側のサイドバーにノート（カードやその他の項目）の数を表示します。<br>
<br>
- <b>"Table content"</b>: 次のいずれかを指定します。<br>
&nbsp&nbsp&nbsp- <i><b>"No interaction"</b></i>: テーブルの内容を操作することはできません。この設定では、Advanced Browserは通常のAnkiブラウザーと同じように動作します。<br>
&nbsp&nbsp&nbsp- <i><b>"Selectable"</b></i>: テーブルの内容を選択できます。ただし、変更はすべて無視されます。この設定を使うと、通常の手順（ノートを選択し、フィールドにマウスを移動し、内容を選択してコピーする）を行わずに、フィールドの内容をすばやくコピーできます。<br>
&nbsp&nbsp&nbsp- <i><b>"Editable"</b></i>: テーブル内で一部の値を直接編集できます。ただし、すべての値を編集できるわけではありません。<br>
</details>
---
<details>
<summary><b>=ZH_CN= 注意事项。点击展开</b></summary>
配置选项如下：<br>
<br>
- <b>"Card Info Dialog Always On Top"</b>：布尔值（即 "true" 或 "false"）。允许在一个始终显示在调用它的窗口上方的独立窗口中显示卡片信息。<br>
<br>
- <b>"Column alignment"</b>：以下选项之一：<br>
&nbsp&nbsp&nbsp- <i><b>"Start"</b></i>：列中的文本左对齐（对于从右向左书写的语言，则右对齐）。<br>
&nbsp&nbsp&nbsp- <i><b>"Center"</b></i>：列中的文本居中对齐。<br>
<br>
- <b>"Hide custom row highlighting"</b>：布尔值（即 "true" 或 "false"）。移除此插件在表格中应用的所有行高亮效果。<br>
<br>
- <b>"Hide the button for which the value is set to one"</b>：字符串。若要隐藏表格上方的所有按钮，请将此值设为 "1"。若只隐藏指定按钮，请在对应的位置（从左向右计数）输入 "1"。例如，"001000000" 会隐藏第三个按钮，同时保留其余八个标准按钮。<br>
<br>
- <b>"Hide the query string used to generate the table"</b>：布尔值（即 "true" 或 "false"）。隐藏表格上方显示的文本，该文本用于说明获取数据时使用的具体查询条件。<br>
<br>
- <b>"Language"</b>：字符串。如果指定空字符串，程序将尝试查找与 Anki 中设置的语言相对应的翻译文件。否则，请指定插件文件夹中的文件名（不包含扩展名，例如俄语使用 "ru"）。文件位置示例："...Anki2\addons21\874215009\advancedbrowser\localization\ru.lng"。可以通过 Anki 打开插件文件夹：工具 -> 插件 -> 选择此插件 -> 点击“查看文件”按钮 -> 进入 "advancedbrowser\localization" 目录。如果没有你的语言版本，请复制 "en.lng" 文件，并使用新语言对应的名称保存，然后用文本编辑器打开，只翻译 === 块之间的文本。<br>
<br>
- <b>"Show internal fields"</b>：布尔值（即 "true" 或 "false"）。启用更多与卡片和笔记相关的数据库内部字段列（开发者选项）。<br>
<br>
- <b>"Show note counts"</b>：布尔值（即 "true" 或 "false"）。在左侧边栏中显示笔记数量（包括卡片和其他元素）。<br>
<br>
- <b>"Table content"</b>：以下选项之一：<br>
&nbsp&nbsp&nbsp- <i><b>"No interaction"</b></i>：无法与表格内容进行交互。这使 Advanced Browser 的行为与 Anki 标准浏览器相同。<br>
&nbsp&nbsp&nbsp- <i><b>"Selectable"</b></i>：可以选择表格内容，但所有更改都会被忽略。此选项非常实用，因为可以快速复制字段内容，而不必按照常规步骤操作（选择笔记、将鼠标移到字段上、选中字段内容，然后复制）。<br>
&nbsp&nbsp&nbsp- <i><b>"Editable"</b></i>：允许直接在表格中编辑部分数值，但并非所有数值都可以编辑。<br>
</details>
---
<details>
<summary><b>=PT_BR= Observações. Clique para expandir</b></summary>
As opções de configuração são:<br>
<br>
- <b>"Card Info Dialog Always On Top"</b>: Valor booleano (ou seja, "true" ou "false"). Permite exibir informações sobre o cartão em uma janela que ficará sempre acima da janela que a abriu.<br>
<br>
- <b>"Column alignment"</b>: Uma das seguintes opções:<br>
&nbsp&nbsp&nbsp- <i><b>"Start"</b></i>: o texto da coluna fica alinhado à esquerda (ou à direita para idiomas escritos da direita para a esquerda).<br>
&nbsp&nbsp&nbsp- <i><b>"Center"</b></i>: o texto da coluna fica centralizado.<br>
<br>
- <b>"Hide custom row highlighting"</b>: Valor booleano (ou seja, "true" ou "false"). Remove qualquer destaque de linhas da tabela aplicado por este complemento.<br>
<br>
- <b>"Hide the button for which the value is set to one"</b>: String de texto. Para ocultar todos os botões acima da tabela, defina o valor como "1". Para ocultar botões específicos, coloque um "1" na posição correspondente (contando da esquerda para a direita). Por exemplo, "001000000" ocultará o terceiro botão, enquanto os outros oito botões padrão continuarão visíveis.<br>
<br>
- <b>"Hide the query string used to generate the table"</b>: Valor booleano (ou seja, "true" ou "false"). Oculta o texto exibido acima da tabela, que informa a consulta específica utilizada para recuperar os dados.<br>
<br>
- <b>"Language"</b>: String de texto. Se uma string vazia for especificada, o programa tentará encontrar um arquivo de tradução para o idioma definido no Anki. Caso contrário, informe o nome do arquivo sem a extensão (por exemplo, "ru" para russo), localizado na pasta do complemento (Exemplo de localização: "...Anki2\addons21\874215009\advancedbrowser\localization\ru.lng"). Você pode abrir a pasta do complemento pelo Anki: Ferramentas -> Complementos -> Selecione o nome deste complemento -> Clique no botão "Ver arquivos" -> Acesse o diretório "advancedbrowser\localization". Se o seu idioma não estiver disponível, crie uma cópia do arquivo "en.lng" com um novo nome (correspondente ao seu idioma), abra-o em um editor de texto e traduza somente o texto entre os blocos ===.<br>
<br>
- <b>"Show internal fields"</b>: Valor booleano (ou seja, "true" ou "false"). Ativa colunas adicionais correspondentes aos campos internos do banco de dados relacionados aos cartões e às notas (opção para desenvolvedores).<br>
<br>
- <b>"Show note counts"</b>: Valor booleano (ou seja, "true" ou "false"). Exibe o número de notas (cartões e outros elementos) na barra lateral esquerda.<br>
<br>
- <b>"Table content"</b>: Uma das seguintes opções:<br>
&nbsp&nbsp&nbsp- <i><b>"No interaction"</b></i>: não é possível interagir com o conteúdo da tabela. Isso faz com que o Advanced Browser funcione como o navegador padrão do Anki.<br>
&nbsp&nbsp&nbsp- <i><b>"Selectable"</b></i>: o conteúdo da tabela pode ser selecionado. Todas as alterações serão ignoradas. Isso é útil porque permite copiar rapidamente o conteúdo dos campos (em vez de seguir o procedimento habitual: selecionar a nota, mover o mouse até o campo, selecionar seu conteúdo e depois copiá-lo).<br>
&nbsp&nbsp&nbsp- <i><b>"Editable"</b></i>: permite editar alguns valores diretamente na tabela, mas não todos.<br>
</details>
