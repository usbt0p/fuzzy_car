1. Conseguir que el coche gire con inputs "simulados"

    Variables a simular:

    Ángulo de giro del volante: Esta es la variable de salida principal.
    - Valores difusos como: "Giro fuerte a la izquierda", "Giro leve a la izquierda", "Sin giro", "Giro leve a la derecha", "Giro fuerte a la derecha".

    - Variable de entrada: Sensores de distancia frontal y laterales: Simular sensores que "midan" la distancia del coche a los lados y al frente.
    Valores pueden ser "Lejos", "Medio", "Cerca", "Muy cerca".
    Necesito los sensores laterales si quiero que sepa a que lado quiere moverse.

    - Reglas tipo:
    Si el sensor izquierdo detecta algo "cerca" → Gira a la derecha "un poco".
    Si el sensor derecho detecta algo "cerca" → Gira a la izquierda "un poco".

    - Variable de entrada: Velocidad del coche: Inicialmente voy a asumir velocidad constante o baja, solo para que gira que gire. La velocidad puede estar entre 0 y un valor fijo (por ejemplo, 10 unidades de velocidad).
    **Problema**: lo que se mueve son los obstáculos, no el coche!!!
    

2. Entorno virtual

    - Espacio de simulación 2D: espacio virtual donde el coche pueda moverse (un grid 2D o un entorno más continuo). Podría ser un mapa de tamaño N×MN×M.

    - Obstáculos: obstáculos simples en el entorno como cuadrados o círculos.
    Posición de los obstáculos: Coordenadas fijas en el espacio????? Se mueven los obstáculos...

    - Implementación: **hay que testear correctamente que pygame tenga todas las capacidades necesarias para los requisitos.**


3. Conseguir que el coche reaccione a obstáculos (no necesariamente con éxito)

    Variables nuevas:

    - Sensores frontales: más sensores para medir la distancia al frente.
    Posibilidad de sensores de largo y corto alcance?

    - Evasión: Esta sería la salida del sistema difuso.
    Si un obstáculo está "muy cerca" al frente, el coche debe intentar girar en una dirección. Hacer que gire "más fuerte"???
    
        > Ejemplo: Si el sensor frontal detecta "muy cerca" → Gira "fuerte" a un lado.
        
        > En esta fase, no es obligatorio que el coche siempre logre evitar el obstáculo; es suficiente que reaccione de alguna manera. Luego voy refinando y ajustando las reglas para que lo haga. Hay que tener en cuenta que probablemente la velocidad influya en la capacidad de reaccionar??

    - Estado del coche: Puede incluir una nueva variable para indicar si el coche ha chocado o no.


4. Conseguir que el coche reaccione con éxito a los obstáculos (fases más adelantadas)

    Ajustes y variables nuevas:

    - Refinamiento de las reglas difusas
        

    - Modificación de velocidad: la velocidad disminuye cuando se detecta un obstáculo cercano.

    - Ángulo de giro dinámico: simular giros más precisos según el ángulo y la proximidad del obstáculo.



5. Implementar acelerador y freno (posible implementación de aparcamiento, muy a futuro y si todo va bien)

    Nuevas variables:

    - Velocidad controlada (freno y acelerador):

    - Sensores traseros:

    - Giros más precisos, marcha atrás

    - Requiere cambiar mucho la interfaz gráfica / implementación del espacio?

---

## **Resumen de ChatGPT + tabla resumen**
        

Resumen de las Variables Clave a Simular en Cada Fase
1. Giro con inputs simulados	Ángulo de giro, Sensores laterales, Velocidad constante	Determina la dirección del coche en base a distancias laterales
2. Entorno virtual	Espacio 2D, Obstáculos, Sensores	Simulación de un entorno con obstáculos y sensores que los detectan
3. Reacción a obstáculos (sin éxito garantizado)	Sensores frontales, Respuesta de evasión, Estado de colisión	Detectar obstáculos y hacer que el coche reaccione, pero sin evitar todos
4. Reacción exitosa a obstáculos	Reglas difusas más complejas, Modificación de velocidad	Ajustar el giro y la velocidad para evitar obstáculos consistentemente
5. Acelerador, freno y aparcamiento	Sensores traseros, Aceleración, Freno, Ángulo de giro para maniobras	Controlar la velocidad, realizar maniobras de aparcamiento usando reglas difusas



| **Fase** | **Variables/Parámetros** | **Descripción** |
|---|---|---|
| **1. Giro con inputs simulados** | Ángulo de giro, Sensores laterales, Velocidad constante | Determina la dirección del coche en base a distancias laterales |
| **2. Entorno virtual** | Espacio 2D, Obstáculos, Sensores | Simulación de un entorno con obstáculos y sensores que los detectan |
| **3. Reacción a obstáculos (sin éxito garantizado)** | Sensores frontales, Respuesta de evasión, Estado de colisión | Detectar obstáculos y hacer que el coche reaccione, pero sin evitar todos |
| **4. Reacción exitosa a obstáculos** | Reglas difusas más complejas, Modificación de velocidad | Ajustar el giro y la velocidad para evitar obstáculos consistentemente |
| **5. Acelerador, freno y aparcamiento** | Sensores traseros, Aceleración, Freno, Ángulo de giro para maniobras | Controlar la velocidad, realizar maniobras de aparcamiento usando reglas difusas |
