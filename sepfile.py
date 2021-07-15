from pdfminer.high_level import extract_text
import psycopg2
import tabula
from tabula import read_pdf
import pandas as pd
from pandas import DataFrame
from flask import Flask, render_template
from flask import request
import os

app = Flask(__name__)

@app.route('/')

def ind():
   return render_template('index.html')
    
@app.route('/tt')
def tt():
    
    # For deleting existing data from table
    URL = "postgres://doslajboilntpo:e55bd2433fac77f5d86037b5d3a27691cc73adf1ba07de17c0c9a91a911c4faa@ec2-54-163-254-204.compute-1.amazonaws.com:5432/de4fue4a8a0q2d"
    conn = psycopg2.connect(URL, sslmode='require')
    cur = conn.cursor()

    query = "DELETE  FROM public.data"
    cur.execute(query)
    conn.commit()


    gdata = request.args.get('value', '') 
    print(gdata)
    gdata=gdata.split(',')
    print(gdata)

    fdata=[]
    fdata=gdata
    
    for i in fdata:
        
        file=i
        txt = extract_text(file)
        txt=txt.split("\n")



            
        if (file=="file0.pdf"):
            g=txt[txt.index("Shipping Date:"):txt.index("CANNA Continental")]
            g=str(g).replace("Shipping Date:","")
            ggg=g.replace("'","")
            ggg=ggg.replace(",","")
            ggg=ggg.replace("[","")
            ggg=ggg.replace("]","")

        else:
            g=txt[txt.index("Shipping Date:"):txt.index("Article")]
            g=str(g).replace("Shipping Date:","")
            ggg=g.replace("'","")
            ggg=ggg.replace(",","")
            ggg=ggg.replace("[","")
            ggg=ggg.replace("]","")
        
        # seperating data            
        a=txt[txt.index("CANNA Continental"):txt.index("Shipping address:")]
        a=str(a).replace("'","")
        aaa=a.replace("[","")
        aaa=aaa.replace("]","")

        b=txt[txt.index("Shipping address:"):txt.index("PACKING LIST")]
        b=str(b).replace("Shipping address:","")
        bbb=b.replace("'","")
        bbb=bbb.replace(",","")
        bbb=bbb.replace("[","")
        bbb=bbb.replace("]","")

        c=txt[txt.index("Customer's address:"):txt.index("Your Reference:")]
        c=str(c).replace("Customer's address:","")
        ccc=c.replace('"',"")
        ccc=ccc.replace("'", "")
        ccc=ccc.replace(",","")
        ccc=ccc.replace("[","")
        ccc=ccc.replace("]","")
        

        d=txt[txt.index("Our Reference:"):txt.index("Carrier:")]
        d=str(d).replace("Our Reference:","")
        ddd=d.replace("'", "")
        ddd=ddd.replace(",", "")
        ddd=ddd.replace("[","")
        ddd=ddd.replace("]","")

        e=txt[txt.index("Your Reference:"):txt.index("Date Ordered:")]
        e=str(e).replace("Your Reference:","")   
        eee=e.replace("'", "")
        eee=eee.replace(",", "")
        eee=eee.replace("[","")
        eee=eee.replace("]","")

        f=txt[txt.index("Date Ordered:"):txt.index("Shipping Date:")]
        f=str(f).replace("Date Ordered:","")
        fff=f.replace("'", "")
        fff=fff.replace(",", "")
        fff=fff.replace("[","")
        fff=fff.replace("]","")
        
        x=[]
        y=[]
        t=[]
        u=[]
        v=[]
        w=[]

        # for file 2
        if (file=="file2.pdf") :
            print(file)
            tables = tabula.read_pdf(file,pages='all',multiple_tables=False)
            
            df = DataFrame(tables[0])
            df_1 = df.iloc[:21,:] 
            df_2 = df.iloc[27:,:]

            df_2[['a','b']] = df['Article'].str.split(n=1, expand=True)

            dff=df_2.drop(['Article','Weight'],axis=1)

            dff.rename(columns = {'Description' : 'Units', 'Units' : 'Quantity','Quantity':'Packages','Packages' : 'Weight','a':'Article','b':'Description'}, inplace = True)

            z = pd.concat([df_1, dff])
            z.reset_index(inplace=True, drop=True) 
            
            zz=DataFrame(z)
            
            for j in range(zz.shape[0]):
                    
                aa=str(zz._get_value(j,'Article'))
                bb=str(zz._get_value(j,'Description'))
                cc=str(zz._get_value(j,'Units'))
                dd=str(zz._get_value(j,'Quantity'))
                ee=str(zz._get_value(j,'Packages'))
                ff=str(zz._get_value(j,'Weight'))

                x.append(aa)
                y.append(bb)
                t.append(cc)    
                u.append(dd)
                v.append(ee)
                w.append(ff)

        else:
            # for other files
            print(file)
            tables = tabula.read_pdf(file,pages='all',multiple_tables=False)
            df = DataFrame(tables[0])
            for j in range(df.shape[0]):
                    
                aa=str(df._get_value(j,'Article'))
                bb=str(df._get_value(j,'Description'))
                cc=str(df._get_value(j,'Units'))
                dd=str(df._get_value(j,'Quantity'))
                ee=str(df._get_value(j,'Packages'))
                ff=str(df._get_value(j,'Weight'))

                x.append(aa)
                y.append(bb)
                t.append(cc)    
                u.append(dd)
                v.append(ee)
                w.append(ff)
        # for removing comma,quotes
        x=str(x).replace(("'nan'"),"")
        x=x.replace("[","")
        x=x.replace("]","")
        x=x.replace("'","")
        y=str(y).replace("'nan'","")
        y=y.replace(",","")
        y=y.replace("[","")
        y=y.replace("]","")
        y=y.replace("'","")
        t=str(t).replace("'nan'","")
        t=t.replace("[","")
        t=t.replace("]","")
        t=t.replace("'","")
        u=str(u).replace("'Total'","")
        u=u.replace("[","")
        u=u.replace("]","")
        u=u.replace("'","")
        

        vv=v.pop()
        v=str(v)
        v=v.replace("[","")
        v=v.replace("]","")
        v=v.replace("'","")
        ww=w.pop()
        w=str(w)
        w=w.replace("[","")
        w=w.replace("]","")
        w=w.replace("'","")
        

        # Inserting data

        q="INSERT INTO public.data(ware,sadd,cadd,oref,yref,sdate,odate,article,description,units,quantity,packages,weight,tpack,tweight) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        records=(aaa,bbb,ccc,ddd,eee,ggg,fff,x,y,t,u,v,w,vv,ww)
        cur.execute(q,records)        
        
        cur.execute("SELECT * FROM public.data")
        data = cur.fetchall()
        conn.commit()
    conn.close()
   
    return render_template('tt.html',data=data)

if __name__ == "__main__":

    app.run(debug=True)




    
     


    


    


