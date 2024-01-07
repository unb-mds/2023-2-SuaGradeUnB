<!-- ## Modelo de Solicitação de Pull Request

Por favor, siga estas etapas antes de enviar um PR.

1. Certifique-se de que seu PR não seja duplicado.

2. Se não for, então certifique-se de que:

a. Você fez suas alterações em um branch separado. Os branches DEVEM ter nomes descritivos que comecem com os prefixos `fix/` ou `task`. Bons exemplos são: `fix/signin-issue`,`task/issue-templates` ou `task/add-search-by-name`.

b. Você sincronizou sua branch com a branch `main` do repositório, para que seu PR possa ser mesclado facilmente.(`git pull origin main`)

c. Você tem mensagens de commit descritivas com um título curto (primeira linha).

d. `make testfull` não gera nenhum erro e possui mais de 90% de *code coverage*. Se ocorrerem erros, corrija-os primeiro e emende seu commit (`git commit --amend`).

3. **Após** essas etapas, você está pronto para abrir um pull request.

a. Dê um título descritivo ao seu PR.

b. Descreva suas alterações.

c. Escreva `closes #XXXX` em seu comentário para fechar automaticamente a issue que seu PR corrige (se houver).

IMPORTANTE: Por favor, revise a paǵina de "COMO CONTRIBUIR?" (https://unb-mds.github.io/2023-2-SuaGradeUnB/contributing/) para obter diretrizes detalhadas sobre contribuições.
-->

# Descrição

<!-- Por favor, inclua um resumo das alterações e a issue relacionada. Também inclua motivação e contexto relevantes. Liste quaisquer dependências necessárias para essa alteração.

Remova o comentário da linha a seguir caso exista uma issue relacionada a seu PR : -->

<!-- **closes #(issue) **-->

## Tipo de alteração

<!-- Por favor, exclua as opções que não são relevantes. -->

* \[ ]   **Bug fix** (alteração que corrige um problema)
* \[ ]   **New feature** (alteração que adiciona funcionalidade)
* \[ ]   **Breaking change** (correção ou funcionalidade que altera o comportamento de outras partes do sistema de maneira significativa)
* \[ ]   **Documentation update** (alteração na documentação)

## Como isso foi testado?

<!-- Por favor, descreva abaixo os testes que você executou para verificar suas alterações. Forneça instruções para que possamos reproduzir. Liste também quaisquer detalhes relevantes para a configuração de seus testes.
Para testes de UI(User Interface), você pode usar uma imagem, GIF ou vídeo para mostrar como o sistema se comporta antes e depois de sua alteração. Você pode usar o [LICEcap](https://www.cockos.com/licecap/) para gravar GIFs facilmente no Windows e MAC ou ferramentas nativas do seu sistema operacional. -->

* \[ ]   Teste A
* \[ ]   Teste B

## Checklist

<!-- Você deve marcar todas as as opções aplicáveis ao seu PR. -->

* \[ ]   Meu código segue as diretrizes de contribuição deste projeto
* \[ ]   Realizei uma revisão pessoal do meu código
* \[ ]   Comentei meu código, especialmente em áreas de difícil compreensão
* \[ ]   Fiz alterações correspondentes na documentação <!--*( caso aplicável)* -->
* \[ ]   Minhas alterações não geram novos *warnings* ou erros
* \[ ]   Adicionei testes que comprovam que minha correção é eficaz ou que minha funcionalidade está funcionando corretamente <!--*( caso aplicável)* -->
* \[ ]   Todos os testes unitários novos e existentes passam localmente com minhas alterações <!-- Use 'make test' ou 'make testfull' -->
