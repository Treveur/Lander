void setup() {
Serial.begin(9600); // set the baud rate
Serial.println("Ready"); // print "Ready" once
pinMode(13, OUTPUT);    
}
void loop() {
char inByte = ' ';
if(Serial.available()){ // only send data back if data has been sent
char inByte = Serial.read(); // read the incoming data
if(inByte == '1'){
  digitalWrite(13, HIGH);  
} else{
  digitalWrite(13, LOW);
}
Serial.println(inByte); // print "Ready" once
}
delay(100); // delay for 1/10 of a second
}
