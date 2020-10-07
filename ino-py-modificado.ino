/* carga y descarga de un capacitor, 
 * Para el ejercicio C= 22 microf, Rcarga=10 kOhm, Rdescarga= 5 kOhm
*/

// Pines usados
#define cargar 13   
#define descargar 11    // descarga auxiliar
#define mideC 0 // pin donde mide V_C
//#define mideRf 5

//unsigned long t0;   // tiempo inicio lecturas
unsigned int valorsensor;
//unsigned int lecturaRf = 0;

//float k = 5.0/1023.0;

void setup () {
  pinMode(cargar, OUTPUT );    // pin de carga  
  pinMode(descargar, OUTPUT ); // pin de descarga auxiliar
  //pinMode(mideRf, INPUT);
  Serial.begin(9600);          // envio dato serial
  valorsensor = analogRead(mideC);
}

void loop(){
  /* Descarga capacitor */
  digitalWrite(cargar, LOW );
  pinMode(descargar, OUTPUT );               
  digitalWrite(descargar, LOW );
  
//  t0 = micros ();                 // tiempo inicial
  valorsensor = analogRead(mideC);
  
  //lecturaRf = analogRead(mideRf);
  while (valorsensor> 0) {
    //Serial.print ( micros ()-t0); // tiempo transcurrido 
    //Serial.print ( "," );
    //Serial.println (valorsensor);
    //valorsensor = analogRead(mideC);

    //Serial.print (( micros ()-t0)*1e-6); Serial.print ( " s descarga," ); // tiempo transcurrido
    Serial.println (valorsensor);//Serial.print ( " V, " );Serial.print (lecturaRf*k);Serial.print ( " V, \t" );
    valorsensor = analogRead (mideC);
    }
  /* carga capacitor */ 
  digitalWrite (cargar, HIGH ); 
  pinMode(descargar, INPUT );    // pin auxiliar con alta impedancia
  //t0 = micros ();                 // tiempo inicial. No haría falta, ver aclaración más abajo
  valorsensor = analogRead (mideC);
  
//  lecturaRf = analogRead(mideRf);
  while (valorsensor <1016) {         // valor maximo de carga de 1024 
    //Serial.print ( micros ()-t0);
    //Serial.print ( "," );
    //Serial.println (valorsensor);
    valorsensor = analogRead (mideC);
// el monitor serial muestra (tiempo en microseg, VC). 
// Entonces tendría que modificar esto para que no se gaste en leer el tiempo si después lo hace python.
// directamente que tire el voltaje (en cuentas):

    //Serial.print (( micros ()-t0)*1e-6); Serial.print ( " s CARGA," ); // tiempo transcurrido
    Serial.println (valorsensor);//Serial.print ( " V, " );Serial.print (lecturaRf*k);Serial.print ( " V, \t" );
    //Serial.println ((lecturaRf+valorsensor)*k);
    valorsensor = analogRead (mideC);
//    lecturaRf = analogRead(mideRf);
  }
  delay(1000);
}
