from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import numpy

def index(request):
    return render(request, 'index.html')

def processpage(request):
    return render(request, 'process.html')
    

def script(request):
    filename = 'Demo.pdf'
    title1 = "Farmers Insurance"
    title2 = "Asset Recovery Analysis"
    logo = 'C:/Users/Tushar/Desktop/NewYork/NewYork/2.jpg'

    pdf = canvas.Canvas(filename, bottomup=0)
    pdf.translate(inch, inch)

    pdf.drawInlineImage(logo, -16, -110, width=290, height=73)

    y = -25
    pdf.setFont('Times-Bold', 11)
    pdf.drawString(330, y, "Bottom Line Concepts, LLC")

    y = y + 10
    pdf.setFont('Times-Roman', 10)
    pdf.drawString(330, y, "1407 Broadway 40th Floor")
    y = y + 10
    pdf.drawString(330, y, "New York NY 10018")

    pdf.setFont('Times-Bold', 10)
    y = y + 16
    pdf.drawString(330, y, "Tel: (212) 668-1111")
    y = y + 10
    pdf.drawString(330, y, "info@bottomlinesavings.com")
    y = y + 10
    pdf.setFont('Times-Roman', 10)
    pdf.drawString(330, y, "www.BottomLineSavings.com")

    y = y + 50
    pdf.setFont('Times-Bold', 16)
    pdf.drawCentredString(220, y, title1)
    y = y + 20
    pdf.drawCentredString(220, y, title2)

    filename = 'C:/Users/Tushar/Desktop/NewYork/Records_nike.csv'
    data = pd.read_csv(filename)

    y = y + 30
    pdf.setFont('Times-Roman', 12)
    pdf.drawString(1, y, "  i)  Estimated Recovery: $1,000,000")
    y = y + 20
    pdf.drawString(1, y, " ii)  Estimated Unclaimed Property ID #s: 2,600 ")
    y = y + 20
    pdf.drawString(1, y, "iii)  Estimated # Agencies Holding Funds: 35")
    y = y + 20
    year = data['Year Reported'].min()
    yr = str(year)
    pdf.drawString(1, y, "iv)  Escheated Funds since " + yr)


    

    owner_Name = data['Owner Name'].unique()
    reported_By = data['Reported By'].unique()
    type_of_Property = data['Type of Property'].unique()

    y = y + 50
    pdf.setFont('Times-Bold', 16)
    pdf.drawString(60, y, "Unclaimed Property Identified - Reported Owner")

    y = y + 30
    col = 0
    for next_link in owner_Name:
        pdf.setFont('Times-Roman', 7)
        if (y < 680):
            if (col % 2 == 0):
                pdf.drawString(1, y, next_link)  
            else:
                pdf.drawString(250, y, next_link)
                y = y+17 
        else:
            pdf.showPage()
            pdf.translate(inch, inch)
            y = 0
            pdf.setFont('Times-Roman', 7)
            if (col % 2 == 0):
                pdf.drawString(1, y, next_link)  
            else:
                pdf.drawString(0, y, next_link)  
                y = y+17
        col = col+1

    y = y + 50
    pdf.setFont('Times-Bold', 16)
    pdf.drawString(70, y, "Unclaimed Property Identified - Reported By")

    y = y + 30
    col = 0
    for next_link1 in reported_By:
        pdf.setFont('Times-Roman', 7)
        if (y < 680):
            if (col % 2 == 0):
                pdf.drawString(1, y, next_link1)  
            else:
                pdf.drawString(250, y, next_link1)
                y = y+17 
        else:
            pdf.showPage()
            pdf.translate(inch, inch)
            y = 0
            pdf.setFont('Times-Roman', 7)
            if (col % 2 == 0):
                pdf.drawString(1, y, next_link1)  
            else:
                pdf.drawString(1, y, next_link1)  
                y = y+17
        col = col+1

    y = y + 50
    pdf.setFont('Times-Bold', 16)
    pdf.drawString(80, y, "Unclaimed Property Identified – Types")

    y = y + 30
    col = 0
    for next_link2 in type_of_Property:
        pdf.setFont('Times-Roman', 7)
        if (y < 680):
            if (col % 2 == 0):
                pdf.drawString(1, y, next_link2)  
            else:
                pdf.drawString(250, y, next_link2)
                y = y+17 
        else:
            pdf.showPage()
            pdf.translate(inch, inch)
            y = 0
            pdf.setFont('Times-Roman', 7)
            if (col % 2 == 0):
                pdf.drawString(1, y, next_link2)  
            else:
                pdf.drawString(1, y, next_link2)  
                y = y+17
        col = col+1
    pdf.save()

    return render(request, 'index.html')


def process(request):
    organization = request.GET.get('organization')
    
    form_data={
    'id4_hf_0' : 0,
    'companyName' : organization,
    'companyCity' : '',
    'search' : 'Search'
    }

    with requests.Session() as s:
        url = "https://ouf.osc.state.ny.us/ouf/"
        r = s.get(url)
        
        soup = BeautifulSoup(r.content, 'html5lib')

        action_url = soup.find('form', id='id2').get('action')

        split_url = action_url.split("/")
        final_url = "https://ouf.osc.state.ny.us/ouf/" + split_url[1] + "&companyName=aa"
        rep = s.post(url=final_url)

        search_soup = BeautifulSoup(rep.content, 'html5lib')
        
        search_action = search_soup.find('form', id='id3').get('action')
    
        filename="Records_nike.csv"
        f= open(filename, "w")

        headers="Owner Name,Owner Address,Reported By,Reported As,Number of Owners,Type of Property,OUF Code,Year Reported\n"
        f.write(headers)
        oldest_year = 2100
        count = 0
        row = 0
        next_page_next = ""
        for x in range(5):
            if(count == 0):
                search_split_url = search_action.split("/")
                search_result_url = "https://ouf.osc.state.ny.us/ouf/" + search_split_url[1] + "/" + search_split_url[2] 
                search_result_rep = s.post(url=search_result_url, data=form_data)
            else:
                next_page_next_url = next_page_next.split("/")
                next_detail_url = "https://ouf.osc.state.ny.us/ouf/" + next_page_next_url[1] + "/" + next_page_next_url[2]
                #print("next " + next_detail_url)
                search_result_rep = s.post(url=next_detail_url)
            
            next_search_result_soup = BeautifulSoup(search_result_rep.content, 'html5lib')
            next_table_body = next_search_result_soup.find('tbody')
            next_hyperlinks = next_table_body.find_all('a')
            
            for next_link in next_hyperlinks:
                if(row % 2 == 0):
                    next_linkText = next_link.get('href')
                
                    next_split_link_url = next_linkText.split("/")
                    next_detail_url = "https://ouf.osc.state.ny.us/ouf/" + next_split_link_url[1] + "/" + next_split_link_url[2]
                    
                    next_rep_detail = s.post(url=next_detail_url)
                    next_info_soup = BeautifulSoup(next_rep_detail.content, 'html5lib')
                    information = next_info_soup.find('div', {"class": "panel-body"}).get_text()
                    
                    val = information.strip('\n')
                    next_information = val.split('\n')

                    owner_name = next_information[2].strip()
                    next_owner_name = ''.join(owner_name.split(','))
                    owner_address = next_information[6].strip()
                    next_owner_address = ''.join(owner_address.split(','))
                    reported_by = next_information[10].strip()
                    next_reported_by = ''.join(reported_by.split(','))
                    reported_as = next_information[14].strip()
                    next_reported_as = ''.join(reported_as.split(','))
                    number_of_owners = next_information[18].strip()
                    next_number_of_owners = ''.join(number_of_owners.split(','))
                    type_of_property = next_information[22].strip()
                    next_type_of_property = ''.join(type_of_property.split(','))
                    ouf_code = next_information[28].strip()
                    next_ouf_code = ''.join(ouf_code.split(','))
                    year_reported = next_information[34].strip()
                    next_year_reported = ''.join(year_reported.split(','))

                    year = int(next_year_reported)
                    if (year < oldest_year):
                        oldest_year = year

                    print("next_owner_name = " + next_owner_name + " next_owner_address = " + next_owner_address + " next_reported_by = " + next_reported_by + " next_reported_as = " + next_reported_as + " next_number_of_owners = " + next_number_of_owners + " next_type_of_property = " + next_type_of_property + "next_ouf_code = " + next_ouf_code + "next_year_reported = " + next_year_reported)
                    f.write(next_owner_name + "," + next_owner_address + "," + next_reported_by + "," + next_reported_as + "," + next_number_of_owners + "," + next_type_of_property + "," + next_ouf_code + "," + next_year_reported + "\n")
                row = row+1
            count = count+1
            #print("Web Scraping for page : ")
            #print(count)

            print("Oldest Year = ")
            print(oldest_year)

            if (next_search_result_soup.find('a', title='Go to next page')):
                next_page_next = next_search_result_soup.find('a', title='Go to next page').get('href')
                #print("next " + next_page_next)
            else:
                break

    f.close()

    filename = 'Demo.pdf'
    title1 = "Farmers Insurance"
    title2 = "Asset Recovery Analysis"
    logo = 'C:/Users/Tushar/Desktop/NewYork/NewYork/2.jpg'

    pdf = canvas.Canvas(filename, bottomup=0)
    pdf.translate(inch, inch)

    pdf.drawInlineImage(logo, -16, -110, width=290, height=73)

    y = -25
    pdf.setFont('Times-Bold', 11)
    pdf.drawString(330, y, "Bottom Line Concepts, LLC")

    y = y + 10
    pdf.setFont('Times-Roman', 10)
    pdf.drawString(330, y, "1407 Broadway 40th Floor")
    y = y + 10
    pdf.drawString(330, y, "New York NY 10018")

    pdf.setFont('Times-Bold', 10)
    y = y + 16
    pdf.drawString(330, y, "Tel: (212) 668-1111")
    y = y + 10
    pdf.drawString(330, y, "info@bottomlinesavings.com")
    y = y + 10
    pdf.setFont('Times-Roman', 10)
    pdf.drawString(330, y, "www.BottomLineSavings.com")

    y = y + 50
    pdf.setFont('Times-Bold', 16)
    pdf.drawCentredString(220, y, title1)
    y = y + 20
    pdf.drawCentredString(220, y, title2)

    filename = 'C:/Users/Tushar/Desktop/NewYork/Records_nike.csv'
    data = pd.read_csv(filename)

    y = y + 30
    pdf.setFont('Times-Roman', 12)
    pdf.drawString(1, y, "  i)  Estimated Recovery: $1,000,000")
    y = y + 20
    pdf.drawString(1, y, " ii)  Estimated Unclaimed Property ID #s: 2,600 ")
    y = y + 20
    pdf.drawString(1, y, "iii)  Estimated # Agencies Holding Funds: 35")
    y = y + 20
    year = data['Year Reported'].min()
    yr = str(year)
    pdf.drawString(1, y, "iv)  Escheated Funds since " + yr)


    

    owner_Name = data['Owner Name'].unique()
    reported_By = data['Reported By'].unique()
    type_of_Property = data['Type of Property'].unique()

    y = y + 50
    pdf.setFont('Times-Bold', 16)
    pdf.drawString(60, y, "Unclaimed Property Identified - Reported Owner")

    y = y + 30
    col = 0
    for next_link in owner_Name:
        pdf.setFont('Times-Roman', 7)
        if (y < 680):
            if (col % 2 == 0):
                pdf.drawString(1, y, next_link)  
            else:
                pdf.drawString(250, y, next_link)
                y = y+17 
        else:
            pdf.showPage()
            pdf.translate(inch, inch)
            y = 0
            pdf.setFont('Times-Roman', 7)
            if (col % 2 == 0):
                pdf.drawString(1, y, next_link)  
            else:
                pdf.drawString(0, y, next_link)  
                y = y+17
        col = col+1

    y = y + 50
    pdf.setFont('Times-Bold', 16)
    pdf.drawString(70, y, "Unclaimed Property Identified - Reported By")

    y = y + 30
    col = 0
    for next_link1 in reported_By:
        pdf.setFont('Times-Roman', 7)
        if (y < 680):
            if (col % 2 == 0):
                pdf.drawString(1, y, next_link1)  
            else:
                pdf.drawString(250, y, next_link1)
                y = y+17 
        else:
            pdf.showPage()
            pdf.translate(inch, inch)
            y = 0
            pdf.setFont('Times-Roman', 7)
            if (col % 2 == 0):
                pdf.drawString(1, y, next_link1)  
            else:
                pdf.drawString(1, y, next_link1)  
                y = y+17
        col = col+1

    y = y + 50
    pdf.setFont('Times-Bold', 16)
    pdf.drawString(80, y, "Unclaimed Property Identified – Types")

    y = y + 30
    col = 0
    for next_link2 in type_of_Property:
        pdf.setFont('Times-Roman', 7)
        if (y < 680):
            if (col % 2 == 0):
                pdf.drawString(1, y, next_link2)  
            else:
                pdf.drawString(250, y, next_link2)
                y = y+17 
        else:
            pdf.showPage()
            pdf.translate(inch, inch)
            y = 0
            pdf.setFont('Times-Roman', 7)
            if (col % 2 == 0):
                pdf.drawString(1, y, next_link2)  
            else:
                pdf.drawString(1, y, next_link2)  
                y = y+17
        col = col+1
    pdf.save()


    return render(request, 'process.html')




