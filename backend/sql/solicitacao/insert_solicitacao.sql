-- Inserir solicitação de sangue do hospital para o hemocentro
-- Parâmetros: Hospital, Hemocentro, QntOPlus, QntOMinus, QntAPlus, QntAMinus, QntBPlus, QntBMinus, QntABPlus, QntABMinus, AceitaNegada
INSERT INTO Solicitacao (Hospital, DataHora, Hemocentro, QntOPlus, QntOMinus, QntAPlus, QntAMinus, QntBPlus, QntBMinus, QntABPlus, QntABMinus, AceitaNegada)
VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
