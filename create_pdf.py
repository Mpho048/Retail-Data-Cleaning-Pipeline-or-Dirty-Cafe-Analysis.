import pandas as pd 
import os
import PIL
from PIL import Image
from pypdf import PdfReader
import fpdf 

make = dir(fpdf.FPDF)
#print(make)
words = []
# don't overwrite any method
for mak in make:
    cc = "get_cols"
    if cc in mak:
        print("Yes", mak)
    else:
        words.append(mak)
print()       
#print(help(fpdf.FPDF.cell))
#==========/======_====//=========

class PDF(fpdf.FPDF):
    """  
    def __init__(self):
        super().__init__()
        self.add_page()
"""        
    def header(self):
         self.set_font("helvetica","B",15)
         self.cell(0,10,"Data Analysis Report", 0,1,)#Don't want it at center
         self.ln(10)
         
    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica","I",7)
        self.cell(0,10,f"Page {self.page_no()}",0,0,"C")

    def Set_title(self,title:str,font:str = "Arial",bg_color = (200,220,255),text_color=(255,255,255),no_color = "N"):
        """Set title
        Args:
            title:str,
            font:str = 'Arial',
            bg_color:tuple =(200,220,255)
            text_color:tuple = (255,255,255)
            no_color:str(Y/N) = "N",   
        """
        self.set_font(font,"B",16)
        if len(no_color) == 1 and no_color.upper() == "Y":
            self.cell(200,10,title,0,1,'C')
            self.ln(5)
        elif len(no_color)  == 1 and no_color == "N":
            self.set_fill_color(*bg_color)
            self.set_text_color(*text_color)
            self.cell(0,25,title,border = 0,ln = 1,align = "C",fill = True)
            self.set_text_color(0,0,0)
            self.ln(10)
        self.set_fill_color(255,255,255)
        
    def write_txt(self,word:str,line= "L",multi = False):
        """Set path to get a font
        Args:
            word:str
            multi:Bool = False (multiple lines)
            line:str/choice[C,R,L] = L
        """
        self.set_font("Arial","B",size = 10)
        if multi:
            self.multi_cell(0,5,word,align = line)
            self.ln()
        else:
            self.cell(0,5,word,align = line)
            self.ln()
        
    def _get_cols(self,df,W,H,size = 9,font = "helvetica",name = "S"):
        """Get Columns Data from DataFrame
        Args:
            size:int = 9
            W:int,
            H:int,
            name(of first col ):str,
            font(font name):str = 'helvetica'
        """
        print("font: ",font)
        self.set_font(family=font,style="B",size=size)
        self.cell(W,H,border = 1,text = name,)
        for col in df.columns:
            self.cell(W,H,str(col),1,0,"C")
        self.ln() 
        
    def single_col(self,df,col = "Cols"):
        """ For a serious
        use form Series to pdf
        data.name  = name
        Args:
            col:str = 'Cols'
            df: pd.Series()
        """
        if df.name == None:
            df.name = "Value"
        data = [(str(col),df.name)]+list(df.items())
        self.set_font("helvetica",size = 12)
        with self.table() as table:
            for index in data:
                row = table.row()
                for val in index:
                    row.cell(str(val))
        self.ln()                
        
    def add_table(self,df):
          #self.add_page()
          self.set_font("helvetica",size = 10)
          #calculate column width (Page width/ number of columns)
          page_width = self.w-2*self.l_margin
          col_width = page_width/len(df.columns)
          line_hieght = self.font_size*2.5
          
          # Table Header(light blue header)
          self.set_fill_color(200,220,255)
          self.set_font("helvetica","B",10)
          for col in df.columns:
              self.cell(col_width, line_hieght, str(col),border = 1,fill=True, align = "C")
          self.ln()
              #Table Rows
          self.set_font("helvetica",size =9)
          for _,rows in df.iterrows():
                for row in rows:
                    self.cell(col_width, line_hieght, str(row),border=1,align="C")
                self.ln()
          
         
    def create_table(self,df,W=35,H=15,size = 9,font ="helvetica",name= "S"):
        """Create a table using pd.DataFrame
        Args:
            df: pd.DataFrame()
            W(width):int = 30,
            H(height):int = 10
            size:int = 9
            name(first rows):str = " "
            font:str = 'helvetica'
          """
        # get columns data
        self._get_cols(df,W,H,size,font,name)
        
        # get value in table
        self.set_font(font,size=size)
        for genre,rows in df.iterrows():
            self.cell(W,H,str(genre),1)
            for row in rows:
                if isinstance(row,(float, int)):
                    val = f"{row:.2f}"
                else:
                    val = str(row)
                self.cell(W,H,val,1,0,"C")
            self.ln()
            
def convert_to_pdf(path,new_name):
    """Conver image to pdf
    Args:
        path(path of the file):str,
        new_name:str,
    """
    if path.lower().endswith(("png","jpg","jpeg",)):
        img = Image.open(path)
        if img.mode == "RGBA":
            img = img.convert("RGB")
        output_path = f"{str(new_name)}.pdf"
        img.save(output_path,"PDF",resolution = 100.0,quality = 50)
        print(f"Document saved to {output_path}")

#need help with this                
def convert_to_png(path,new_name):
    """Convert images to png
    Args:
        path:str,
        new_name:str
    """
    if path.lower().endswith(("png","jpeg", "jpg")):
       img = Image.open(path)
       output_path = f"{new_name}.png"
       img.save(output_path,"PNG",)
       print(f"Document saved:{output_path}")

                
                                                            
                                                                                                                                                            