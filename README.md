# Análisis de Datos Olímpicos - Prueba Técnica Verbum

## Autor: Martín Ramírez

## Decisiones y justificaciones

### 1. Estrategia de imputación

El dataset presenta valores faltantes en varias columnas críticas:

- Age: 3.49% faltante
- Height: 22.19% faltante
- Weight: 23.19% faltante
- Medal: 85.33% faltante

**Soluciones adoptadas**:

#### Age

El porcentaje de datos faltantes es bajo (3.49%), y la mediana es robusta ante valores atípicos

#### Height y Weight

Se utilizó imputación con mediana agrupada por Sexo y Deporte. Estas variables están fuertemente correlacionadas con el sexo y tipo de deporte

Además se usó como fallback a mediana global si el grupo no tiene datos

#### Medal

Se hizo conversión de NaN a categoría "No Medal". Con 85.33% de datos faltantes, la imputación introduciría demasiado ruido

### 2. Datos Duplicados

Se encontraron dos tipos de duplicación:

1. Filas exactamente iguales (0.51%): Eliminadas por ser redundantes
2. IDs repetidos con datos diferentes: Conservados, representan atletas en múltiples eventos

Además se eliminó la columna ID por generar confusión, ya que no identifica filas únicas sino atletas individuales. Ateriormente se determinó que ID es exactamente igual a Name en términos de usabilidad para identificar al atleta.

## Configuración del entorno y ejecución

Solo re requiere un entorno virtual y instalar las dependencias de requirements.txt

Para las pruebas con la API REST hay que inicializar el server de desarrollo en Flask con `python app.py`. Para probar la API

La API estará disponible en: `http://localhost:5000`

## Ubicación de Archivos Generados

Al ser un proyecto tan pequeño, todos los archivos generados se encuentran en la raíz del proyecto:

## API endpoints

Ambas API están creadas como se pidió. A continuación hay algunos ejemplos de su uso:

### Atletas por NOC

```bash
curl "http://localhost:5000/athlete_data_by_noc?noc=CHI"
```

**Respuesta**:

```json
{
    "data": [
        {
            "Medal": "No Medal",
            "Name": "Carlos Abarca Gonzlez",
            "Sport": "Boxing",
            "region": "Chile"
        },
        ...
        {
            "Medal": "No Medal",
            "Name": "Luis Zuiga",
            "Sport": "Boxing",
            "region": "Chile"
        }
    ],
    "noc": "CHI",
    "region": "Chile",
    "total_records": 752
}
```

### KPI

```bash
curl "http://localhost:5000/kpi"
```

```json
{
  "analysis_period": "2000-present",
  "metrics": {
    "Athletics": 26.0,
    "Football": 24.567251461988302,
    "Swimming": 22.6891495601173
  },
  "sports_count": 3
}
```

## Visualizaciones

Las visualizaciones están disponibles en el Notebook (`process.ipynb`):

## Desafíos Enfrentados

Hubo un alto porcentaje de valores faltantes (especialmente medallas: 85%). Además la columna ID no era única por fila, generando confusión y en general los datos no estaban del todo pulcros. Aún así me tomé la libertad de manejar los datos como pensé que los querrían. En un caso tan desprolijo preguntaría antes de hacer suposiciones.

## Limitaciones Actuales

Sé que la aplicación no es perfecta, pero prioricé cumplir con los requisitos. Sé que hay áreas mejorables. Por ejemplo la escalabilidad se podría mejorar implementando algún tipo de paginación y base de datos para consultar la API.

También si el pipeline incluyese archivos más diversos habría que validar las entradas y manejar los errores que derivarían de ello.
