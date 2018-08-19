Los archivos .txt poseen los datasets, empleados para las fases de entrenamiento y de pruebas, estas fases se ejecutan una tras la otra empleando el programa PSMergeCNFSingTrainTestThenReviseIW.m, que a su vez manda a llamar a la función PSMergeDNFSingletonsmu2.m.
CNForalcaADCSGE-GSTM.txt: Hasta el momento, el que produce mejor accuracy (78.95) con 7 atributos: age, alcohol drinking, betel quid chewing, smoking, GSTM, gender and ethnicity. Por cierto, en el artículo An Application of Belief Merging for the Diagnosis of Oral Cancer existe una fe de errattas, dice GSTT debe decir GSTM en el parrafo que menciona los atributos que producen la mayor accuracy.

CNForalcaADCSGE-GSTT.txt: Produce una accuracy de 77.19 con 7 atributos: age, alcohol drinking, betel quid chewing, smoking, GSTT, gender and ethnicity.

CNForalcancer: Produce una accuracy de 71.93 con los 8 atributos existentes: age, alcohol drinking, betel quid chewing, smoking, GSTT, GSTM, gender and ethnicity.

CNForalcaADCSGE.txt: Produce una accuracy de 68.42 con 6 atributos: age, alcohol drinking, betel quid chewing, smoking, gender and ethnicity.

CNForalcaADCSG.txt: Produce una accuracy de 49.12 con 5 atributos: age, alcohol drinking, betel quid chewing, smoking and gender.

CNForalcaADCS.txt: Produce una accuracy de 49.12 con 4 atributos: age, alcohol drinking, betel quid chewing and smoking.

Hay archivos intermedios que se crean durante el proceso de entrenamiento y de pruebas con extensiones: .tra, .tes, .dnf, .B01 y .sol y con el mismo nombre de su dataset. Por ejemplo, durante el procesamiento de CNForalcancer.txt se crean los archivos: 

CNForalcancer.tra: archivo que contiene los casos de entrenamiento. A partir de CNForalcancer.txt se toman los registros: 1,2,4,5,7,8,10,11,13,14, ... para integrar este archivo.

CNForalcancer.tes: archivo que contiene los casos para realizar las pruebas. A partir de CNForalcancer.txt se toman los registros: 3,6,9,12,15, ... para integrar este archivo.
 
CNForalcancer.dnf: archivo que contiene el sistema de diagnóstico, es decir, la fusión de creencias de los datos del archivo .tra.
  
CNForalcancer.B01: archivo que contiene las pruebas intermediarias empleando el archivo .dnf, las respuestas que son contradictoria o que no tiene respuesta pasan a un proceso de revisión tratar de disolver la contradicción u obtener una respuesta. La primera columna indica B si no es posible responder como falso o 0 si es posible responder como falso a la pregunta ¿Tiene cáncer? La segunda columna indica B si no es posible responder como verdadero o 1 si es posible responder como verdadero a la pregunta ¿Tiene cáncer? En caso de que en el mismo renglón exista un 0 y un 1 en la primera y segunda columnas, respectivamente, indica que se responde a la pregunta como verdadero y falso, lo que representa una contradicción. La tercera y última columna indica el valor que posee el caso en el dataset.

CNForalcancer.sol: archivo que contiene la solución final para cada uno de los 57 casos de prueba, el primer parámetro es el obtenido por el sistema de diagnóstico y el segundo es el que inicialmente posee el archivo .txt.

maripozos@gmail.com