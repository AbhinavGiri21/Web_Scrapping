from flask import Flask,render_template,request,jsonify
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import logging


logging.basicConfig(filename="scrapper.log",level=logging.INFO)
app=Flask(__name__)
@app.route("/",methods=['GET'])

def homepage():
    return render_template("index.html")

@app.route("/review",methods=['POST','GET'])
def index():
    if request.method=='POST':
        try:
            searchstring=request.form['content'].replace(" ","")
            flipcart_url="https://www.flipkart.com/search?q="+searchstring 
            urlclient=urlopen(flipcart_url)
            flipcart_page=urlclient.read()
            urlclient.close()
            flipcart_html=bs(flipcart_page,'html.parser')
            bigbox=flipcart_html.findAll("div",{"class","_1AtVbE col-12-12"})
            del bigbox[0:3]
            box=bigbox[0]
            product_link="https://www.flipkart.com/search?q="+box.div.div.div.a['href']
            product_req=requests.get(product_link)
            product_html=bs(product_req.text,'html.parser')
            print(product_html)
            comment_box=product_html.find_all("div",{"class":"_16PBlm"})
            del comment_box[0:2]
            comment_box=product_html.find_all('div', {'class': "_16PBlm"})
            filename=searchstring+".csv"
            f=open(filename,"w")
            headers="Product,Customer Name,Rating,Heading,Comment\n"
            f.write(headers)
            reviews=[]
            for comment in comment_box:
                try:
                    name=comment.div.div.find_all('p',{'class':"_2sc7ZR _2V5EHH"})[0].text
                except:
                    logging.info("name")

                try:
                    rating=comment.div.div.div.div.text
                except:
                    rating = 'No Rating'
                    logging.info("rating")

                try:
                    commentHead=comment.div.div.div.p.text
                except:
                    commentHead='No Comment Heading'
                    logging.info(commentHead)
                try:
                    comtag=comment.div.div.find_all('div', {'class': ''})
                    custComment=comtag[0].div.text
                except Exception as e:
                    logging.info(e)

                mydict={"Product":searchstring,"Name":name,"Rating":rating,"CommentHead":commentHead,
                          "Comment":custComment}
                reviews.append(mydict)
            logging.info("log my final result {}".format(reviews))
            return render_template('result.html',reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
        else:
            return render_template('index.html')
if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)
        
