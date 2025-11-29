-- Autenticar usuário por login e senha
-- Parâmetros: Login, Senha
-- Retorna: Role (Papel)
SELECT Role
FROM Usuario
WHERE Login = %s AND Senha = %s;
