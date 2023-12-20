#!/usr/bin/env python3

import requests
import json
import pandas as pd
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import sys

def get_anime_news_by_id(id):
	response = requests.get(f'https://api.jikan.moe/v4/anime/{id}/news')
	return response.json() if response.status_code == 200 else None

def extract():
	animes_df = pd.read_csv('animes_id.csv')

	animes_news = []

	for anime_id in animes_df['anime_id']:
		
		news_json = get_anime_news_by_id(anime_id)

		if news_json is not None:
			news_data = news_json['data']

			for i in range(min(len(news_data), 3)):
				news = news_data[i]
				anime_news = {'url': news['url'], 
							  'title': news['title'], 
							  'date': news['date'], 
							  'image': news['images']['jpg']['image_url'],
							  'summary': news['excerpt']
				}

				animes_news.append(anime_news)


	animes_news.sort(key = lambda news: news['date'], reverse = True)

	return animes_news

def send(news, email_src, email_dest):
	html = """
			<h1> Novas notícias de seus animes </h1>
			<table>
				<tr>
					<th> Data </th>
					<th> URL </th>
					<th> Title </th>
					<th> Image </th>
					<th> Summary </th>
				</tr>
				{BODY}
			</table>
	"""

	body = ''.join([
		f"""
			<tr>
				<td>{item['date']}</td>
				<td>{item['url']}</td>
				<td>{item['title']}</td>
				<td><img width = "50px" height = "50px" src = \"{item['image']}\"></td>
				<td>{item['summary']}</td>
			</tr>
		"""
		for item in news
	])

	html = html.replace('{BODY}', body)

	message = Mail(
    from_email = email_src,
    to_emails = email_dest,
    subject = 'últimas notícias dos seus animes',
    html_content = html)

	try:
		sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
		response = sg.send(message)
		print(response.status_code)
		print(response.body)
		print(response.headers)
	except Exception as e:
		print(e)

def main():

	if len(sys.argv) < 3:
		print('use: python3 main.py <email-remetente> <email-destinatário>')
		sys.exit(0)

	email_src = sys.argv[1]
	email_dest = sys.argv[2]

	load_dotenv()

	news = extract()

	news.sort(key = lambda anime: anime['date'], reverse = True)

	send(news, email_src, email_dest)

if __name__ == '__main__':
	main()
