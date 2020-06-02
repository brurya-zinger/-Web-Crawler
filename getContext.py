from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient


class MyClass:
    def __init__(self):
        self.time = ""
        self.brand = ""
        self.model = ""
        client = MongoClient()
        db = client.my_data_base
        self.collection = db.test_collection
        self.l2 = []

# receive the metadata
    def extracting_data(self,newUrl1, is_add_data=True):
        html_content1 = requests.get(newUrl1).text
        soup1 = BeautifulSoup(html_content1, "xml")
        try:
            self.time = soup1.find(class_="field field-name-changed-date field-type-ds field-label-inline clearfix").find(class_="field-item even").text
        except:#There is no such class in this path
            self.time = soup1.find(class_="field field-name-changed-date field-type-ds field-label-hidden").find(class_="field-items").find("div",class_="field-item even").text
        self.brand =soup1.find(class_="field field-name-field-brand field-type-taxonomy-term-reference field-label-inline clearfix").find(class_="field-item even").text
        self.model=soup1.find(class_="field field-name-field-model field-type-text field-label-inline clearfix").find(class_="field-item even").text
        if is_add_data: # add to db
            self.add_data(self.time,self.brand,self.model)
        else: # for update
            self.compere(self.time,self.brand,self.model)
# add data to db
    def add_data(self, a, b, c):
        client = MongoClient()
        db = client.my_data_base
        collection = db.test_collection
        post = {"timeUpdate": a,
                "brand": b,
                "model": c}
        result = self.collection.insert_one(post)
# print the db
    def print1(self):
        for x in self.collection.find():
            print(x)
# delete db
    def delete_all(self):
        x = self.collection.delete_many({})


    def extract_data(self):
         x = self.collection.find()
         l1 = []
         for i in x:
             del i['_id']# delete the key
             l1.append(i)
         # print(l1, type(l1))
         return l1


    def compere(self, a,b,c):
        post = {"timeUpdate": a,
                "brand": b,
                "model": c}
        self.l2.append(post)


# Extract the paths of the name data  from the  NAME column in the table
# is_add_data=True default,if false  we're in the process of updating the db
    def geting_url(self, is_add_data=True):
        url="https://www.rockchipfirmware.com/firmware-downloads"
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, "xml")
        for tag in set(soup.find_all("td", class_="views-field views-field-title")):
            for i in tag.find_all(True):
                if i.has_attr('href'):
                    tag = i['href'].replace('\\','/')
                    newUrl = "https://www.rockchipfirmware.com//{}".format(tag)
                    self.extracting_data(newUrl,is_add_data)#extract the data from the information page


        if not is_add_data:
            return self.l2




    def update_information(self,s1,s2):
        # the difference  between the list
        to_delete = [item for item in s1 if item not in s2]
        to_update = [item for item in s2 if item not in s1]

        if(to_delete != []):
            for item in to_delete:
                self.collection.delete_many(item)

        if(to_update != []):
            for item in to_update:
                self.collection.insert_one(item)


def main():
    mata = MyClass()
    mata.delete_all()
    # mata.geting_url()
    mata.print1()
    #for update the new information in the database....
    s1 = mata.extract_data()
    s2 = mata.geting_url(False)
    mata.update_information(s1, s2)



    # #  for the test  i  added
    # s1 = mata.extract_data() + [{'timeUpdate': 'Sunday, March 31, 1900 - 19:06', 'brand': 'Cube', 'model': 'U20GT-WS'}]
    # # # s2 contains a list of the data
    # s2 = mata.geting_url(False) + [{'timeUpdate': 'Sunday, March 30, 1960 - 19:06', 'brand': 'Cube', 'model': 'U20GT-WS'}]
    # mata.update_information(s1, s2)
    # s3 = mata.extract_data()
    #
    # to_delete = [item for item in s3 if item not in s2]
    # to_update = [item for item in s3 if item not in s1]
    # # print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    # print(to_delete)
    # # print('------------------------------------------------------')
    # print(to_update)





if __name__ == '__main__':
    main()





