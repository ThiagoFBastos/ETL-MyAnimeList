# ETL do MyAnimeList

ETL alimentado pela API não oficial do MyAnimeList([Jikan](https://docs.api.jikan.moe/)) e que usa o SendGrid para enviar
as informações de um email para outro. Mais especificamente, dado um arquivo csv com os ID's de algums animes o 
programa realiza uma requisição GET em https://api.jikan.moe/v4/anime/{id}/news para obter notícias relacionadas ao anime
alvo, armazenando no máximo 3, e após isso envia de um email para outro uma mensagem com uma tabela html com algumas informações 
dessas notícias.

![ScreenShot](https://github.com/ThiagoFBastos/ETL-MyAnimeList/blob/main/screenshot.png)

## Requisitos
- biblioteca requests
- biblioteca sendgrid
- biblioteca pandas
- biblioteca dotenv

## Instruções

1. Instale as bibliotecas dependentes
2. Crie uma conta no SendGrid e configure para poder enviar emails
3. Gere o token do SendGrid
4. Crie um arquivo .env e coloque isso nele:
	```
	SENDGRID_API_KEY="{TOKEN do SendGrid}"
	```
5. No terminal digite python3 main.py [email remetente] [email-destinatário]
	- Exemplo:
	```
		python3 main.py origem@gmail.com destino@gmail.com
	``` 
