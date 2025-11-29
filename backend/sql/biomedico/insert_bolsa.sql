-- Inserir um registro de bolsa de sangue testada por biomédico
-- Parâmetros: Codigo, VolumeDoado, TipoSangue, Valido, Triagem, Biomedico, Hemocentro, DataTestagem
INSERT INTO BolsaSangue (Codigo, VolumeDoado, TipoSangue, Valido, Triagem, Biomedico, Hemocentro, DataTestagem)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
