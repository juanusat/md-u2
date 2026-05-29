# Muestra del dataset

**Primeras 10 y últimas 10 líneas del dataset**

```
periodo_anio_mes;periodo_estado;prestador_nombre;prestador_cargo_fijo;prestador_aplica_igv;prestador_estado;localidad_nombre;localidad_tiene_factor_ajuste;localidad_valor_factor_ajuste;localidad_consumo_promedio;localidad_estado;eett_no
mbre;eett_resolucion;eett_fec_ini_vig;eett_estado;clase_nombre;categoria_nombre;eett_categoria_volumen_asignado;rango_ini;rango_fin;rango_tiene_scf;rango_fin_scf;tarifa_agua;tarifa_alcanta
202401;Historico;EMAPA HVCA S.A.;1.5444;SI;Activo;HUANCAVELICA;SI;0.75;11.45684324;Activo;EETT-2019-2024-EMAPA HVCA S.A.;Resolucion Nro. 057-2018-SUNASS-CD;20181223;Activo;No residencial;Comercial y otros;30.00;0;30;NO;;1.8288;0.4058
202401;Historico;EMAPA HVCA S.A.;1.5444;SI;Activo;HUANCAVELICA;SI;0.75;11.45684324;Activo;EETT-2019-2024-EMAPA HVCA S.A.;Resolucion Nro. 057-2018-SUNASS-CD;20181223;Activo;No residencial;Comercial y otros;30.00;30;;NO;;2.3115;0.5132
202401;Historico;EMAPA HVCA S.A.;1.5444;SI;Activo;HUANCAVELICA;SI;0.75;11.45684324;Activo;EETT-2019-2024-EMAPA HVCA S.A.;Resolucion Nro. 057-2018-SUNASS-CD;20181223;Activo;No residencial;Estatal;50.00;0;50;NO;;1.212;0.2692
202401;Historico;EMAPA HVCA S.A.;1.5444;SI;Activo;HUANCAVELICA;SI;0.75;11.45684324;Activo;EETT-2019-2024-EMAPA HVCA S.A.;Resolucion Nro. 057-2018-SUNASS-CD;20181223;Activo;No residencial;Estatal;50.00;50;;NO;;1.8288;0.4058
202401;Historico;EMAPA HVCA S.A.;1.5444;SI;Activo;HUANCAVELICA;SI;0.75;11.45684324;Activo;EETT-2019-2024-EMAPA HVCA S.A.;Resolucion Nro. 057-2018-SUNASS-CD;20181223;Activo;No residencial;Industrial;80.00;0;;NO;;2.3115;0.5132
202401;Historico;EMAPA HVCA S.A.;1.5444;SI;Activo;HUANCAVELICA;SI;0.75;11.45684324;Activo;EETT-2019-2024-EMAPA HVCA S.A.;Resolucion Nro. 057-2018-SUNASS-CD;20181223;Activo;Residencial;Doméstico;20.00;0;8;SI;8;0.842;0.187
202401;Historico;EMAPA HVCA S.A.;1.5444;SI;Activo;HUANCAVELICA;SI;0.75;11.45684324;Activo;EETT-2019-2024-EMAPA HVCA S.A.;Resolucion Nro. 057-2018-SUNASS-CD;20181223;Activo;Residencial;Doméstico;20.00;8;20;NO;;0.9086;0.2016
202401;Historico;EMAPA HVCA S.A.;1.5444;SI;Activo;HUANCAVELICA;SI;0.75;11.45684324;Activo;EETT-2019-2024-EMAPA HVCA S.A.;Resolucion Nro. 057-2018-SUNASS-CD;20181223;Activo;Residencial;Doméstico;20.00;20;;NO;;1.1273;0.2505
202401;Historico;EMAPA HVCA S.A.;1.5444;SI;Activo;HUANCAVELICA;SI;0.75;11.45684324;Activo;EETT-2019-2024-EMAPA HVCA S.A.;Resolucion Nro. 057-2018-SUNASS-CD;20181223;Activo;Residencial;Social;6.00;0;10;NO;;0.2056;0.0451
202401;Historico;EMAPA HVCA S.A.;1.5444;SI;Activo;HUANCAVELICA;SI;0.75;11.45684324;Activo;EETT-2019-2024-EMAPA HVCA S.A.;Resolucion Nro. 057-2018-SUNASS-CD;20181223;Activo;Residencial;Social;6.00;10;;NO;;0.5093;0.1126
202603;Historico;EMAPACOP S.A.;3.6;NO;Activo;PUCALLPA;SI;0.65;21.46512832;Activo;EETT-2025-2029-EMAPACOP S.A.;Resolucion Nro. 041-2024-SUNASS-CD;2024718;Activo;Residencial;Doméstico;25.00;8;20;NO;;1.27;0.64
202603;Historico;EMAPACOP S.A.;3.6;NO;Activo;PUCALLPA;SI;0.65;21.46512832;Activo;EETT-2025-2029-EMAPACOP S.A.;Resolucion Nro. 041-2024-SUNASS-CD;2024718;Activo;Residencial;Doméstico;25.00;20;;NO;;2.22;1.12
202603;Historico;EMAPACOP S.A.;3.6;NO;Activo;PUCALLPA;SI;0.65;21.46512832;Activo;EETT-2025-2029-EMAPACOP S.A.;Resolucion Nro. 041-2024-SUNASS-CD;2024718;Activo;Residencial;Social;35.00;0;;NO;;0.53;0.27
202603;Historico;EPS EMSAPA CALCA S.A.;1.6;SI;Activo;CALCA;SI;0.8;14.04;Activo;EETT-2025-2027-EPS EMSAPA CALCA S.A.;Resolucion Nro. 049-2024-SUNASS-CD;2024823;Activo;No residencial;Comercial y otros;30.00;0;;NO;;1.29;0.24
202603;Historico;EPS EMSAPA CALCA S.A.;1.6;SI;Activo;CALCA;SI;0.8;14.04;Activo;EETT-2025-2027-EPS EMSAPA CALCA S.A.;Resolucion Nro. 049-2024-SUNASS-CD;2024823;Activo;No residencial;Estatal;50.00;0;;NO;;1.29;0.24
202603;Historico;EPS EMSAPA CALCA S.A.;1.6;SI;Activo;CALCA;SI;0.8;14.04;Activo;EETT-2025-2027-EPS EMSAPA CALCA S.A.;Resolucion Nro. 049-2024-SUNASS-CD;2024823;Activo;No residencial;Industrial;100.00;0;;NO;;1.29;0.24
202603;Historico;EPS EMSAPA CALCA S.A.;1.6;SI;Activo;CALCA;SI;0.8;14.04;Activo;EETT-2025-2027-EPS EMSAPA CALCA S.A.;Resolucion Nro. 049-2024-SUNASS-CD;2024823;Activo;Residencial;Doméstico;15.00;0;10;SI;10;0.85;0.14
202603;Historico;EPS EMSAPA CALCA S.A.;1.6;SI;Activo;CALCA;SI;0.8;14.04;Activo;EETT-2025-2027-EPS EMSAPA CALCA S.A.;Resolucion Nro. 049-2024-SUNASS-CD;2024823;Activo;Residencial;Doméstico;15.00;10;20;NO;;1.16;0.2
202603;Historico;EPS EMSAPA CALCA S.A.;1.6;SI;Activo;CALCA;SI;0.8;14.04;Activo;EETT-2025-2027-EPS EMSAPA CALCA S.A.;Resolucion Nro. 049-2024-SUNASS-CD;2024823;Activo;Residencial;Doméstico;15.00;20;;NO;;1.29;0.24
202603;Historico;EPS EMSAPA CALCA S.A.;1.6;SI;Activo;CALCA;SI;0.8;14.04;Activo;EETT-2025-2027-EPS EMSAPA CALCA S.A.;Resolucion Nro. 049-2024-SUNASS-CD;2024823;Activo;Residencial;Social;15.00;0;;NO;;0.68;0.14
```