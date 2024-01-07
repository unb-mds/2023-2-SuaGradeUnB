## Modelo de Solicitação de Pull Request

Por favor, siga estas etapas antes de enviar um PR.

1.  Certifique-se de que seu PR não seja duplicado.

2.  Se não for, então certifique-se de que:

   a. Você fez suas alterações em um branch separado. Os branches DEVEM ter nomes descritivos que comecem com os prefixos `fix/` ou `task`. Bons exemplos são: `fix/signin-issue`,`task/issue-templates` ou `task/add-search-by-name`.

   b. Você sincronizou sua branch com a branch `main` do repositório, para que seu PR possa ser mesclado facilmente.(`git pull origin main`)

   c. Você tem mensagens de commit descritivas com um título curto (primeira linha).

   d. `make testfull` não gera nenhum erro e possui mais de 90% de *code coverage*. Se ocorrerem erros, corrija-os primeiro e emende seu commit (`git commit --amend`).

3.  **Após** essas etapas, você está pronto para abrir um pull request.

   a. Dê um título descritivo ao seu PR.

   b. Descreva suas alterações.

   c. Coloque `closes #XXXX` em seu comentário para fechar automaticamente a issue que seu PR corrige (se houver).

IMPORTANTE: Por favor, revise a paǵina de [COMO CONTRIBUIR ?](https://unb-mds.github.io/2023-2-SuaGradeUnB/contributing/) para obter diretrizes detalhadas sobre contribuições.

**POR FAVOR, REMOVA O MODELO ACIMA ANTES DE ENVIAR**

# Descrição

Por favor, inclua um resumo das alterações e a issue relacionada. Também inclua motivação e contexto relevantes. Liste quaisquer dependências necessárias para essa alteração.

**closes # (issue)** (*caso exista*)

## Tipo de alteração

Por favor, exclua as opções que não são relevantes.

  * \[ ] Bug fix (alteração que corrige um problema)
  * \[ ] New feature (alteração que adiciona funcionalidade)
  * \[ ] Breaking change (correção ou funcionalidade que altera o comportamento de outras partes do sistema de maneira significativa)
  * \[ ] Documentation update (alteração na documentação)

# Como isso foi testado?

Por favor, descreva os testes que você executou para verificar suas alterações. Forneça instruções para que possamos reproduzir. Liste também quaisquer detalhes relevantes para a configuração de seus testes.

  * \[ ] Teste A
  * \[ ] Teste B

# Checklist:

  * \[ ] Meu código segue as diretrizes de contribuição deste projeto
  * \[ ] Realizei uma revisão pessoal do meu código
  * \[ ] Comentei meu código, especialmente em áreas de difícil compreensão
  * \[ ] Fiz alterações correspondentes na documentação *( se necessário)*
  * \[ ] Minhas alterações não geram novos *warnings* ou erros
  * \[ ] Adicionei testes que comprovam que minha correção é eficaz ou que minha funcionalidade está funcionando corretamente
  * \[ ] Testes unitários novos e existentes passam localmente com minhas alterações
