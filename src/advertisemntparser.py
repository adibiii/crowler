from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.soup = None

    @property
    def price(self):
        price_tag = self.soup.find('span', attrs={'class': 'price'})
        if price_tag:
            return price_tag.string

    @property
    def title(self):
        title_tag = self.soup.find('span', id='titletextonly')
        if title_tag:
            return title_tag.string

    @property
    def post_id(self):
        post_id_tag = self.soup.select_one('body > section > section > section > div.postinginfos > p:nth-child(1)')
        if post_id_tag:
            return post_id_tag.text.replace('post id: ', '')

    @property
    def body(self):
        body_tag = self.soup.find('section', id='postingbody')
        if body_tag:
            return body_tag.text

    @property
    def creat_time(self):
        time_tag = self.soup.select_one('body > section > section > section > div.postinginfos > p.postinginfo.reveal > time')
        if time_tag:
            return time_tag.text

    def parse(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        data_dict = {
            'title': self.title, 'price':  self.price,
            'body': self.body, 'post_id': self.post_id,
            'created_time': self.creat_time
        }
        return data_dict


