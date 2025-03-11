## Ejecución de tests unitarios

Durante el desarrollo del ejercicio se utilizó una suite de tests para validar los resultados de algunos casos de interés.
Esta misma utiliza el paquete `Pytests`, por lo que primero es necesario instalar las dependencias indicadas en el archivo `requirements.txt`. 
Para ello, se debe ejecutar el siguiente comando en la terminal:
```bash
pip install -r requirements.txt
```

Una vez ejecutado y parados sobre la raiz del directorio del ejercicio, se debe ejecutar el siguiente comando para correr los tests:
```bash
pytest
```

Esto ejecutará todos los tests unitarios en el archivo `minesweeper_test.py` y mostrará los resultados en la terminal.