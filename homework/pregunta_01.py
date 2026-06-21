def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.

    """
    import pandas as pd
    import re

    # Leemos el archivo completo
    with open('files/input/clusters_report.txt', 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    datos = []
    fila_actual = None

    # Las primeras 4 líneas son el encabezado y la línea punteada (-------)
    for linea in lineas[4:]:
        # Si la línea empieza con uno o más espacios seguidos de un número, es un nuevo cluster
        if re.match(r'^\s*\d+', linea):
            # Si ya estábamos procesando una fila, la guardamos antes de empezar la nueva
            if fila_actual:
                datos.append(fila_actual)

            # Extraemos: (cluster) (cantidad) (porcentaje)% (texto)
            coincidencia = re.search(r'^\s*(\d+)\s+(\d+)\s+([\d\,?\.?]+)\s*%\s+(.*)', linea)
            if coincidencia:
                cluster = int(coincidencia.group(1))
                cantidad = int(coincidencia.group(2))
                # Reemplazamos coma por punto por si los decimales vienen en formato europeo
                porcentaje = float(coincidencia.group(3).replace(',', '.'))
                palabras = coincidencia.group(4).strip()
                
                fila_actual = [cluster, cantidad, porcentaje, palabras]
                
        elif linea.strip():
            # Si la línea no empieza con número pero tiene contenido, son más palabras clave
            if fila_actual:
                fila_actual[3] += ' ' + linea.strip()

    # No olvidemos agregar la última fila procesada
    if fila_actual:
        datos.append(fila_actual)

    # Aplicamos la limpieza solicitada a las palabras clave
    for fila in datos:
        texto = fila[3]
        # Eliminamos el punto final si el texto termina con uno
        texto = texto.rstrip('.')
        # Aseguramos separación por coma y un solo espacio
        texto = ', '.join([palabra.strip() for palabra in texto.split(',')])
        # Reemplazamos cualquier espacio múltiple interno por uno solo
        texto = ' '.join(texto.split())
        
        fila[3] = texto

    # Nombres de columnas según las reglas indicadas
    columnas = [
        'cluster',
        'cantidad_de_palabras_clave',
        'porcentaje_de_palabras_clave',
        'principales_palabras_clave'
    ]

    # Construimos el DataFrame
    df = pd.DataFrame(datos, columns=columnas)

    return df