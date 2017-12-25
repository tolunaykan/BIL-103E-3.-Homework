
#####################################################################
### Assignment skeleton
### You can alter the below code to make your own dynamic website.
### The landing page for assignment 3 should be at /
#####################################################################

from bottle import route, run, default_app, debug, static_file, request, error
import csv

contents = []
with open("a3_input.csv") as input_file:
    for row in csv.reader(input_file):
        contents = contents + [row]

def htmlify(title,anaTablo,filterKey,stringTable,toplam):
    page = '''
        <!doctype html>
        <html lang="en">
         <head>
          <meta charset="utf-8" />
          <title>{0}</title>
          <link rel="stylesheet" type="text/css" href="static/style.css" />
         </head>
         <body>
          <div class="headImage">
           <img src="static/headImage.jpg">
          </div>
          <div class="navDiv">
           <ul>
	        <li class="home"><a href="/">Home</a></li>
            <li class="centerLi"><p>Number of cinema audiences according to years</p></li>
	        <li class="rightLi" style="float:right;">
	         <div class="sonli">
              <p>{4}</p>
	          <div class="searchBarDiv">
	           <form action="/searchBar" method="GET">
                <input type="submit" value="Search">	   
	            <input type="text" name="search" placeholder="Enter city name">
	           </form>
	          </div>
	         </div>
	        </li>
	       </ul> 
	      </div>
          <div class="main">
           <div class="formsAll">
            <div class="solFormlar">
             <div class="formDivLeft">
              <fieldset>
	           <legend class="legends">Sort by</legend>
	           <form class="siralaClass" action="/sorttable" method="POST">
	            {2}<br><br>
	            <input type="radio" name="filter" value=">" checked> > <br>
                <input type="radio" name="filter" value="<"> < <br><br>
	            <input value="Sort" type="submit"> 
               </form>
              </fieldset>
             </div>
             <div class="formDivCenter">
              <fieldset>
               <legend class="legends">Search City</legend>
	           <form action="/searchCity" method="GET">
                Please enter city name: <br>   
                <input style="margin-top:2%" type="text" name="cityname" placeholder="City name"><br><br>	   
                <select name="functions" size="3" multiple>
                 <option value="total">Get Total</option>
                 <option value="average">Get Average</option>
                 <option value="cinema">Is there cinema?</option>
                </select><br><br>
	            <input type="submit" value="Search">	   
	           </form>
              </fieldset>	
             </div>
            </div>
            <div class="sagFormlar">
             <div class="resultRightForm">
              {3}
             </div>
             <div class="formDivRight">
              <fieldset>
	           <legend class="legends">Statistics</legend>
	           <form action="/statistics" method="POST">
	            <input type="text" name="citynumber" placeholder="Top X city"><br><br>
	            <input type="checkbox" name="total" value="total">Total<br>
	            <input type="checkbox" name="average" value="average">Average<br><br>
	            Choose years you want<br>
	            <select style="margin-top:2%" name="years" size="4" multiple>
	             <option value="1">2006</option>
		         <option value="2">2007</option>
        		 <option value="3">2008</option>
        		 <option value="4">2009</option>
        		 <option value="5">2010</option>
        		 <option value="6">2011</option>
        		 <option value="7">2012</option>
        		 <option value="8">2013</option>
        		 <option value="9">2014</option>
        		 <option value="10">2015</option>
        		 <option value="11">2016</option>
	            </select><br><br>
	            <input type="submit" value="Search">
	           </form>
              </fieldset>	
             </div>
         </div>
        </div>
        <div class="contents">
         {1}
        </div>
       </div>
      </body>
     </html>
    '''.format(title,anaTablo,sortSelectorHtmlify(filterKey),stringTable,toplam)
    return page

def getTable(icerik):
    tabledata="""
     <table>
      <tbody>
    """
    isGreen=1
    for datarow in range(0,len(icerik)):
        rowstring="\t<tr>\n"
        if isGreen==1:
            rowstring="\t<tr class='transactions2'>\n"
        else:
            rowstring="\t<tr class='transactions'>\n"
        for item in icerik[datarow]:
            if datarow==0:
                rowstring+="\t\t<th class='tableHead'>%s</th>\n" % item
            else:
                rowstring+="\t\t<td>%s</td>\n" % item
        tabledata+=rowstring
        if isGreen==1:
            isGreen=0
        else:
            isGreen=1
    tabledata+="""
          </tbody>
         </table>
        """        
    return tabledata

def sortSelectorHtmlify(filterKey): 
    stringSelector='<select name="sort">'
    for i in contents[0]:
        if filterKey==i:
            stringSelector+="<option value='{0}' selected>{1}</option>".format(i,i)
        else:
            stringSelector+="<option value='{0}'>{1}</option>".format(i,i)
    stringSelector+="</select>"  
    return stringSelector 
   
def sortTable():
     value = request.POST['sort']
     valueFilter= request.POST['filter']
     if value and value=="Cities":
         sira = "Cities"
     elif value and value != "Cities":
         sira = int(value)-2005
     else:
         sira = "Cities"  
     icerik = contents.copy()
     firstItem = icerik.pop(0)
     if sira=="Cities":
         content = sorted(icerik, key=lambda x: x[0], reverse=False)
     else:
         content = sorted(icerik, key=lambda x: int(x[sira]), reverse=True)
     if(valueFilter=="<"):
        content.reverse()   
     content.reverse()
     content.append(firstItem)
     content.reverse()
     return htmlify("Sorted by "+value,getTable(content),value," "," ")
     
def searchTable():
    nameValue = request.GET['cityname']
    if nameValue=="":
        nameValue="Istanbul"
    functionsList = request.GET.getlist('functions')
    cityList=[]
    for row in contents:
        if nameValue==row[0]:
            cityList.append(row.copy())
            break 
    cityList.append(contents[0].copy())
    cityList.reverse()
    veriler = (cityList[1]).copy()
    del veriler[0]
    if "total" in functionsList:
        cityList[0].append("Total")
        cityList[1].append(getTotal(veriler))
    if "average" in functionsList:
        cityList[0].append("Average")
        yilSayisi = len(contents[0])-1
        average = (getTotal(veriler)//yilSayisi)
        cityList[1].append(average)     
    if "cinema" in functionsList:
        cityList[0].append("Cinema")
        cityList[1].append(getIsThereCinema(veriler))
    return htmlify(nameValue,getTable(cityList),"Cities"," "," ")   

def statisticsTable():
    citynumber = request.POST["citynumber"]
    totalCheckBox = request.POST.get("total","none")
    averageCheckBox = request.POST.get("average","none")
    if citynumber=="":
        citynumber=1;
    selectorList = request.POST.getlist('years')
    if not selectorList:
        selectorList = ["1","2","3","4","5","6","7","8","9","10","11"]
    toplam=0
    for item in contents[1:int(citynumber)+1]:
        for i in selectorList:
            toplam+=int(item[int(i)])
    average = toplam//(len(selectorList)*int(citynumber))
    contentsCopy = contents.copy()
    aralikList = (contentsCopy[:int(citynumber)+1])
    liste=[]
    for itemm in aralikList:
        rangim = range(0,len(itemm))
        listeItem=[]
        listeItem.append(itemm[0])
        for i in rangim:
            if str(i) in selectorList:
                listeItem.append(itemm[i])        
        liste.append(listeItem)        
    stringTable= getStatisticsResultTable(totalCheckBox,averageCheckBox,toplam,average)   
    return htmlify("Statistics",getTable(liste),"Cities",stringTable," ") 

def getSearchBarResult():
    nameValue = request.POST.get("search","Istanbul")
    toplam=0
    for row in contents:
        if nameValue in row:
            for item in row[1:]:
                toplam+= int(item)         
    return htmlify("Search",getTable(contents),"Cities"," ","Total: "+ str(toplam))            
        
def getStatisticsResultTable(totalCheckBox,averageCheckBox,toplam,average):
    stringTable="""
     <fieldset>
	  <legend>Result</legend> 
      <table class="result">
	   <tbody>
    """
    if totalCheckBox !="none":
        stringTable+= """
          <tr>
		   <td>Total</td>
		   <td>{0}</td>
		  </tr>
        """.format(toplam)
    if averageCheckBox !="none":
        stringTable+="""
          <tr>
		   <td>Average</td>
		   <td>{0}</td>
		  </tr> 
        """.format(average)
    stringTable+="""
       </tbody>
	  </table>
     </fieldset>
    """    
    return stringTable
     
def getTotal(listTotal):
    toplam=0
    for item in listTotal:
        toplam+= int(item)
    return toplam
    
def getIsThereCinema(icerik):
    isThere=""
    for item in icerik:
        if(item=="0"):
            isThere="&#x2716;"
        else:
            isThere="&#x2714;"
            break
    return isThere    
        
def index():
    return htmlify("Home",getTable(contents),"Cities"," "," ")

@route('/static/<filename>')
def server_static(filename):
  return static_file(filename, root='./static/')

route('/', 'GET', index)
route('/sorttable', 'POST', sortTable)
route('/searchCity', 'GET', searchTable)
route('/statistics', 'POST', statisticsTable)
route('/searchBar', 'GET', getSearchBarResult)

#####################################################################
### Don't alter the below code.
### It allows this website to be hosted on Heroku
### OR run on your computer.
#####################################################################

# This line makes bottle give nicer error messages
debug(True)
# This line is necessary for running on Heroku
app = default_app()
# The below code is necessary for running this bottle app standalone on your computer.
if __name__ == "__main__":
  run()