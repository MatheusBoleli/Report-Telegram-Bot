# Report-Telegram-Bot

Esse foi um projeto elaborado para uso de uma empresa de Telecom, especificamente para enviar certos reports de KPI de seu CallCenter para um grupo do Telegram, todos os dados necessários são extraidos de um site especifico através de um script em Selenium que baixa uma planilha do site. Essa planilha é tratada em pandas, e seus dados consolidados são incluidos em uma mensagem e enviados em um report via telegram.

Para facilitar o uso caso queira adaptar, segue informações uteis abaixo: 

link para buscar IDS do telegram: https://api.telegram.org/bot<YourBOTToken>/getUpdates

Para utilizar a API, é necessário criar um bot no telegram e utilizar seu token gerado no link acima. Ao acessar esse link, sempre que realizar alguma ação com o bot (Enviar mensagens, inclui-lo em grupos e etc) alguns dados em formato JSON serão exibidos, dentre eles o mais util, que será utilizado para essa automação, o groupId, que será exibido ao adicionar o bot em um grupo.
  
Importante frisar, o codigo desse projeto foi criado para uso corporativo, logo seus dados de acesso e sites foram removidos, portanto se trata apenas de um codigo que pode ser adaptado, mas por si só, não é mais funcional.
