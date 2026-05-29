# Diccionario de datos

```yaml
- variable: periodo_anio_mes
  descripcion: "Periodo de referencia de la estructura tarifaria, correspondiente a la fecha en que la tarifa entra en aplicación."
  tipo_dato: Texto
  tamano: 8
  informacion_adicional: "Periodo de referencia de la estructura tarifaria en formato de año y mes: aaaamm. Ejemplo: 202401 corresponde al 1 de enero de 2024."

- variable: periodo_estado
  descripcion: "Condición del periodo tarifario en función de su vigencia."
  tipo_dato: Texto
  tamano: 6
  informacion_adicional: "Valores posibles: Vigente (periodo actualmente aplicable) o Histórico (periodo que ya no se encuentra vigente)."

- variable: prestador_nombre
  descripcion: "Nombre oficial de la empresa prestadora de los servicios de agua potable y saneamiento."
  tipo_dato: Texto
  tamano: 50
  informacion_adicional: "Corresponde a la denominación registrada del prestador ante la Sunass."

- variable: prestador_cargo_fijo
  descripcion: "Monto del cargo fijo aplicado al usuario de agua potable y saneamiento, asociado a costos fijos del servicio que no dependen del nivel de consumo."
  tipo_dato: Numérico
  tamano: 10
  informacion_adicional: "El cargo fijo comprende costos relacionados con actividades como lectura de medidores, facturación, actualización del catastro comercial y cobranza, conforme al Reglamento de Tarifas aprobado por la Sunass."

- variable: prestador_aplica_igv
  descripcion: "Indica si al importe facturado por el servicio se le aplica el Impuesto General a las Ventas (IGV)."
  tipo_dato: Texto
  tamano: 2
  informacion_adicional: "Valores posibles: Si, No."

- variable: prestador_estado
  descripcion: "Situación operativa de la empresa prestadora de servicio de agua potable y saneamiento."
  tipo_dato: Texto
  tamano: 2
  informacion_adicional: "Valores posibles: Activo, Inactivo."

- variable: localidad_nombre
  descripcion: "Nombre de la localidad donde se aplica la estructura tarifaria."
  tipo_dato: Texto
  tamano: 50
  informacion_adicional: "Corresponde al ámbito geográfico atendido por el prestador."

- variable: localidad_tiene_factor_ajuste
  descripcion: "Indica si la localidad cuenta con un factor de ajuste tarifario asociado a criterios socioeconómicos."
  tipo_dato: Texto
  tamano: 2
  informacion_adicional: "Valores posibles: Si, No."

- variable: localidad_valor_factor_ajuste
  descripcion: "Valor numérico del factor de ajuste aplicado a la tarifa del servicio de agua potable en la localidad."
  tipo_dato: Numérico
  tamano: 10
  informacion_adicional: "Puede presentar valores nulos cuando: 1. El factor no ha sido determinado en el estudio tarifario. 2. La empresa prestadora no brinda el servicio en la localidad."

- variable: localidad_consumo_promedio
  descripcion: "Promedio del volumen de consumo de agua potable registrado en la localidad."
  tipo_dato: Numérico
  tamano: 15
  informacion_adicional: "Expresado en metros cúbicos (m³)."

- variable: localidad_estado
  descripcion: "Estado de la localidad respecto a la aplicación de la estructura tarifaria."
  tipo_dato: Texto
  tamano: 2
  informacion_adicional: "Valores posibles: Activo, Inactivo."

- variable: eett_nombre
  descripcion: "Periodo de vigencia del estudio tarifario aprobado para el prestador."
  tipo_dato: Texto
  tamano: 50
  informacion_adicional: "Corresponde a los años de aplicación del estudio tarifario."

- variable: eett_resolucion
  descripcion: "Resolución del Consejo Directivo de la Sunass que aprueba el estudio tarifario."
  tipo_dato: Texto
  tamano: 50
  informacion_adicional: "Incluye el número y año de la resolución correspondiente."

- variable: eett_fec_ini_vig
  descripcion: "Fecha de inicio de vigencia del estudio tarifario aprobado."
  tipo_dato: Fecha
  tamano: 8
  informacion_adicional: "Formato: aaaammdd."

- variable: eett_estado
  descripcion: "Estado de la estructura tarifaria asociada al estudio tarifario."
  tipo_dato: Texto
  tamano: 6
  informacion_adicional: "Valor esperado: Activo."

- variable: clase_nombre
  descripcion: "Clasificación de la unidad de uso según el tipo de actividad desarrollada"
  tipo_dato: Texto
  tamano: 15
  informacion_adicional: "Valores posibles: Residencial, No residencial."

- variable: categoria_nombre
  descripcion: "Categoría tarifaria asignada a la unidad de uso en función de la actividad económica o social."
  tipo_dato: Texto
  tamano: 25
  informacion_adicional: "Valores posibles: Comercial, Comercial y otros, Comercial y otros I, Comercial y otros II, Doméstico, Doméstico I, Doméstico II, Doméstico subsidiado, Estatal, Industrial, Social. Definición y clasificación conforme al Reglamento de Calidad de la Prestación de los Servicios de Saneamiento."

- variable: eett_categoria_volumen_asignado
  descripcion: "Volumen de agua asignado a usuarios no micromedidos para efectos de facturación."
  tipo_dato: Texto
  tamano: 50
  informacion_adicional: "Expresado en metros cúbicos (m³), calculado en función del consumo promedio de usuarios micromedidos de la misma categoría."

- variable: rango_ini
  descripcion: "Valor inicial del rango de consumo al que se aplica una tarifa determinada."
  tipo_dato: Numérico
  tamano: 5
  informacion_adicional: "Expresado en metros cúbicos (m3)."

- variable: rango_fin
  descripcion: "Valor final del rango de consumo hasta el cual se aplica la tarifa correspondiente."
  tipo_dato: Numérico
  tamano: 5
  informacion_adicional: "Expresado en metros cúbicos (m3). Los valores vacíos corresponden a un valor ilimitado."

- variable: rango_tiene_scf
  descripcion: "Indica si en el rango de consumo se aplica el subsidio cruzado focalizado."
  tipo_dato: Texto
  tamano: 2
  informacion_adicional: "Valores posibles: Si, No."

- variable: rango_fin_scf
  descripcion: "Límite máximo del consumo al que se aplica el subsidio cruzado focalizado."
  tipo_dato: Numérico
  tamano: 2
  informacion_adicional: "Expresado en metros cúbicos (m3). Puede presentar valores vacíos cuando rango_tiene_scf = 'No', dado que en estos casos no aplica subsidio cruzado focalizado ni un límite máximo asociado."

- variable: tarifa_agua
  descripcion: "Tarifa aplicable al consumo de agua potable dentro del rango definido."
  tipo_dato: Numérico
  tamano: 15
  informacion_adicional: "Monto expresado en soles por metro cúbico (S/ por m³)."

- variable: tarifa_alcanta
  descripcion: "Tarifa aplicable al servicio de saneamiento dentro del rango de consumo."
  tipo_dato: Numérico
  tamano: 15
  informacion_adicional: "Monto expresado en soles por metro cúbico (S/ por m³)."
```