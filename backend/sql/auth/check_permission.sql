-- Verificar se o papel (role) tem permissão específica (RBAC)
-- Parâmetros: Role, PermissaoNome
-- Retorna: 1 se a permissão existir, nada caso contrário
SELECT 1
FROM RolePermissao RP
JOIN Permissao P ON RP.PermissaoId = P.Id
WHERE RP.Role = %s AND P.Nome = %s;
