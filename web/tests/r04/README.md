# Recuperação da seleção (M8–R04)

O rascunho usa `sessionStorage` (`suagrade:selected-classes:v1`) e guarda somente
período, códigos e identificadores. A restauração espera os períodos oferecidos
e busca as turmas na API; informações removidas não voltam à seleção. A troca de
período invalida a seleção anterior. O formulário mantém a proteção existente:
é necessário remover as turmas antes de escolher outro período.

Inclusões, remoções e limpeza são gravadas pelas ações do usuário, sem efeito
que possa gravar o estado vazio inicial. Uma nova ação cancela a aplicação de
uma restauração pendente. Falha da API preserva o rascunho para outra recarga e
exibe mensagem; falha do armazenamento mantém a seleção em memória.

## Executar a verificação

Use Node >= 20. Em `web/`, instale a aplicação e inicie o servidor:

```sh
npm ci
npm run dev -- --hostname 127.0.0.1 --port 3046
```

Em outro terminal, também em `web/`:

```sh
npm --prefix tests/r04 ci
npm --prefix tests/r04 exec -- playwright install chromium
BASE_URL=http://127.0.0.1:3046 VARIANTE=depois FONTE=.. EVIDENCIAS=/tmp/r04-evidencias node tests/r04/verificar.cjs
npm run lint
```

O roteiro verifica a interface real em Chromium (1366×900 e celular emulado
390×844 com toque). As respostas de API são interceptadas com `massa.json`:
nenhuma conta ou base real é necessária. Evidências e metadados são gravados
em `EVIDENCIAS/depois`. Cada contexto começa com armazenamento limpo.

Na origem `3d399e745383b05e8e3b1a7c97ac0fdbf93a0360`, execute o mesmo roteiro
de uma cópia separada com `VARIANTE=antes`, apontando `FONTE` e `BASE_URL` para
esse checkout e servidor. Essa modalidade confirma a perda e a ausência de
diálogo. Os testes adicionais são executados apenas em `VARIANTE=depois`.

São verificações funcionais da correção; não são uma nova avaliação integral
de M8 nem uma sessão com usuários em celular físico. `sessionStorage` cobre a
aba atual durante a sessão; não oferece salvamento na conta ou sincronização.
Uma aba aberta com `opener` pode receber uma cópia inicial do armazenamento do
navegador. O teste de outra aba usa uma aba independente, sem `opener`.

## Limite conhecido da origem

Com tipos de rotas gerados pelo Next, `tsc --noEmit` falha em
`.next/types/app/layout.ts` porque `app/layout.tsx` exporta `poppins` e
`chivoMono`. O mesmo erro ocorre no checkout original, sem esta correção.
Esse problema preexistente fica fora do escopo de R04.
