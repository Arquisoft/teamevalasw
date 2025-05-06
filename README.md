## Programa para la evaluación entre miembros del mismo grupo

### Archivos de configuración

- **data.xlsx**. Hoja de cálculo con cuatro columnas. user (tiene que coincidir con un usuario del archivo anterior), name, surname, group (grupo al que pertenece el usuario), language (en ó es).
- **users.txt**. Una fila por cada usuario, en el formato usuario:pass (este archivo se puede generar automáticamente).

### Generación automática de los archivos necesarios

Podemos generar todo lo necesario a partir de la hoja de cálculo con los alumnos. Simplemente hay que ejecutar el script

```bash
python generate_data_files.py
```

### Como ejecutarlo

- Crear un entorno virtual y activarlo:

```bash
python -m venv .venv
source .venv/bin/activate
```

- Instalar las dependencias

```bash
pip install -r requirements
```

- Ejecutar

```bash
python app.py
```
