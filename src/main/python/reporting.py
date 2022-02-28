class GeneratePDF():
    def __init__(self,data):
        super().__init__()
        self.data = data
        
    def siteSpecific(self):
        row = f"""
            <tr>
                <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                <td style="border-top: 1px solid #000000; border-left: 1px solid #000000" align="left" valign=bottom><font color="#000000">Risk(s) assessed</font></td>
                <td style="border-top: 1px solid #000000; border-right: 1px solid #000000" colspan=2 align="left" valign=bottom><font color="#000000">{', '.join(self.data["assessments"])}</font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
            </tr>
            <tr>
                <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                <td style="border-left: 1px solid #000000" align="left" valign=bottom><font color="#000000">Sector</font></td>
                <td style="border-right: 1px solid #000000" colspan=2 align="left" valign=bottom><font color="#000000">{self.data["info"]['sector']}</font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
            </tr>
            <tr>
                <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                <td style="border-left: 1px solid #000000" align="left" valign=bottom><font color="#000000">Unit under assessment</font></td>
                <td style="border-right: 1px solid #000000" colspan=2 align="left" valign=bottom><font color="#000000">{self.data["info"]['unit']}</font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
            </tr>
            <tr>
                <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                <td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000" align="left" valign=bottom><font color="#000000">Material of construction</font></td>
                <td style="border-bottom: 1px solid #000000; border-right: 1px solid #000000" colspan=2 align="left" valign=bottom><font color="#000000">{self.data["material"]}</font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
                <td align="left" valign=bottom><font color="#000000"><br></font></td>
            </tr>
        """
        return row
    
    def waterSpecific(self):
        row = ""

        for item in self.data["inputs"]:
            value = 0
            units = "N/A"
            if(type(item[1]) == bool):
                    value = "YES" if item[1] == True else "NO"
            else:
                value = f'{round(item[1],2)}'
            try:
                units = self.data["units"][item[0]]['unit'][0]
            except Exception as e:
                units = self.data["units"][item[0]]['unit']
            row += f"""
                <tr>
                    <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                    <td style="border-top: 1px solid #000000; border-left: 1px solid #000000" align="left" valign=bottom><font color="#000000">{item[0]}</font></td>
                    <td style="border-top: 1px solid #000000" align="left" valign=bottom><font color="#000000">{units}</font></td>
                    <td style="border-top: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF"">{value}</td>
                    <td align="left" valign=bottom><font color="#000000"><br></font></td>
                    <td align="left" valign=bottom><font color="#000000"><br></font></td>
                    <td align="left" valign=bottom><font color="#000000"><br></font></td>
                    <td align="left" valign=bottom><font color="#000000"><br></font></td>
                    <td align="left" valign=bottom><font color="#000000"><br></font></td>
                    <td align="left" valign=bottom><font color="#000000"><br></font></td>
                </tr>
            """


        return row

    def results(self):
        
        table = ""
        for keyValue, items in self.data["report_data"].items():
            i = 0
            row = ""
            for param, item in items.items():
                if(item["Risk"] == "Unacceptable"):
                    bgColor = "#FF0000"
                    fgColor = "#000000"
                elif(item["Risk"] == "Tolerable"):
                    bgColor = "#FFFF00"
                    fgColor = "#000000"
                elif(item["Risk"] == "Acceptable"):
                    bgColor = "#92D050"
                    fgColor = "#000000"
                else:
                    bgColor = "#00B0F0"
                    fgColor = "#000000"
                try:
                    value = round(item["Index"],2)
                except Exception as e:
                    value = item["Index"]
                row += f"""
                    <tr><td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                    """
                if(i < 1):
                    row += f'<td style="border-left: 1px solid #000000" align="left" valign=middle bgcolor="#FFFFFF"><font color="#000000">{keyValue}</font></td>'

                else:
                    row += '<td style="border-left: 1px solid #000000" height="19" align="left" valign=bottom><font color="#000000"><br></font></td>'

                row += f"""
                    <td align="left" valign=middle bgcolor="#FFFFFF"><font color="#000000">{param}</font></td>
                    <td align="center" valign= bgcolor="#FFFFFF""><font color="#000000">{value}</font></td>
                    <td align="center" valign=middle bgcolor={bgColor}><font color={fgColor}><span>{item["Risk"]}</span></font></td>
                    <td colspan=2 align="left" valign=middle bgcolor="#FFFFFF"><font color="#000000"><span>{item["Description"]}</span></font></td>
                    <td style="border-right: 1px solid #000000" colspan=2 align="left" valign=middle bgcolor="#FFFFFF"><font color="#000000"><span>{item["Treatment"]}</span></font></td>
                </tr>
                
                """
                i = i + 1
            row += f"""
                    <tr>
                        <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-left: 1px solid #000000; border-bottom: 1px solid #000000" height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-bottom: 1px solid #000000" height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-bottom: 1px solid #000000" height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-bottom: 1px solid #000000" height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-bottom: 1px solid #000000" height="19" align="left" colspan=2 valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-bottom: 1px solid #000000; border-right: 1px solid #000000" height="19" align="left" colspan=2 valign=bottom><font color="#000000"><br></font></td>
                    </tr>
                    """
            table += row
        return table
    def generateHTML(self):


        html= f"""
            <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    
                    <style type="text/css">
                        body,div,table,thead,tbody,tfoot,tr,th,td,p{{font-family:"Calibri"; font-size:small}}
                        a.comment-indicator:hover + comment{{background:#ffd; position:absolute; display:block; border:1px solid black; padding:0.5em;}} 
                        a.comment-indicator{{background:red; display:inline-block; border:1px solid black; width:0.5em; height:0.5em;}} 
                        comment{{display:none;}} 
                    </style>
                    
                </head>

                <body>

                <table cellspacing="0" border="0">
                    <colgroup width="24"></colgroup>
                    <colgroup width="215"></colgroup>
                    <colgroup width="177"></colgroup>
                    <colgroup width="99"></colgroup>
                    <colgroup width="21"></colgroup>
                    <colgroup width="91"></colgroup>
                    <colgroup width="110"></colgroup>
                    <colgroup width="67"></colgroup>
                    <colgroup width="136"></colgroup>
                    <colgroup width="198"></colgroup>
                    <tr>
                        <td height="28" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td colspan=9 align="center" valign=bottom bgcolor="#3B3838"><b><font size=4 color="#FFFFFF">Risk-based Water Quality Guidelines for Industrial Use</font></b></td>
                        </tr>
                    <tr>
                        <td height="28" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td colspan=9 align="center" valign=bottom bgcolor="#3B3838"><b><font size=4 color="#FFFFFF">Fitness for Use assessment report</font></b></td>
                        </tr>
                    <tr>
                        <td height="28" align="left" valign=bottom bgcolor="#FFFFFF"><font color="#000000"><br></font></td>
                        <td align="center" valign=bottom bgcolor="#FFFFFF"><b><font size=4 color="#FFFFFF"><br></font></b></td>
                        <td align="center" valign=bottom bgcolor="#FFFFFF"><b><font size=4 color="#FFFFFF"><br></font></b></td>
                        <td align="center" valign=bottom bgcolor="#FFFFFF"><b><font size=4 color="#FFFFFF"><br></font></b></td>
                        <td align="center" valign=bottom bgcolor="#FFFFFF"><b><font size=4 color="#FFFFFF"><br></font></b></td>
                        <td align="center" valign=bottom bgcolor="#FFFFFF"><b><font size=4 color="#FFFFFF"><br></font></b></td>
                        <td align="center" valign=bottom bgcolor="#FFFFFF"><b><font size=4 color="#FFFFFF"><br></font></b></td>
                        <td align="center" valign=bottom bgcolor="#FFFFFF"><b><font size=4 color="#FFFFFF"><br></font></b></td>
                        <td align="center" valign=bottom bgcolor="#FFFFFF"><b><font size=4 color="#FFFFFF"><br></font></b></td>
                        <td align="center" valign=bottom bgcolor="#FFFFFF"><b><font size=4 color="#FFFFFF"><br></font></b></td>
                    </tr>
                    <tr>
                        <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-top: 1px solid #000000; border-left: 1px solid #000000" align="left" valign=bottom><font color="#000000">Date:</font></td>
                        <td style="border-top: 1px solid #000000" align="left" valign=bottom sdval="44320" sdnum="1033;1033;D-MMM-YY"><font color="#000000">{self.data['user']['company']}</font></td>
                        <td style="border-top: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-top: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-top: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-top: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-top: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-top: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-top: 1px solid #000000; border-right: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                    </tr>
                    <tr>
                        <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-left: 1px solid #000000" align="left" valign=bottom><font color="#000000">Full Name:</font></td>
                        <td align="left" valign=bottom sdnum="1033;1033;D-MMM-YY"><font color="#000000">{self.data['user']['fullName']}</font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-right: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                    </tr>
                    <tr>
                        <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-left: 1px solid #000000" align="left" valign=bottom><font color="#000000">Position:</font></td>
                        <td align="left" valign=bottom ><font color="#000000">{self.data['user']['role']}</font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-right: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                    </tr>
                    <tr>
                        <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-left: 1px solid #000000" align="left" valign=bottom><font color="#000000">Location:</font></td>
                        <td align="left" valign=bottom ><font color="#000000">{self.data['user']['company']}</font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-right: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                    </tr>
                    
                    <tr>
                        <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000" align="left" valign=bottom><font color="#000000">Contact Details:</font></td>
                        <td style="border-bottom: 1px solid #000000" align="left" valign=bottom sdnum="1033;1033;D-MMM-YY"><u><font color="#0563C1"><a href={self.data['user']['email']}>{self.data['user']['email']}</a></font></u></td>
                        <td style="border-bottom: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-bottom: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-bottom: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-bottom: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-bottom: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-bottom: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-bottom: 1px solid #000000; border-right: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                    </tr>
                    <tr>
                        <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-left: 1px solid #000000" align="left" valign=bottom><font color="#000000">Comments:</font></td>
                        <td align="left" valign=bottom ><font color="#000000">{self.data['user']['description']}</font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td style="border-right: 1px solid #000000" align="left" valign=bottom><font color="#000000"><br></font></td>
                    </tr>
                    <tr>
                        <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom sdnum="1033;1033;D-MMM-YY"><u><font color="#0563C1"><br></font></u></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                    </tr>
                    <tr>
                        <td height="24" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><b><font size=4 color="#3B3838">Assessment Criteria</font></b></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                    </tr>
                    <!-- ***********************************************************************************************************Assessment Criteria************************************************************* -->
                    {self.siteSpecific()}
                    <tr>
                        <td height="24" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><b><font size=4 color="#3B3838">Water Quality inputs</font></b></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                    </tr>
                    <!-- ***********************************************************************************************************Water Quality Inputs************************************************************* -->
                    <tr>
                        <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><b><font color="#181717">Paramemter</font></b></td>
                        <td align="left" valign=bottom><b><font color="#181717">Units</font></b></td>
                        <td align="left" valign=bottom><b><font color="#181717">Value</font></b></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                    </tr>
                    {self.waterSpecific()}
                    <tr>
                        <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                    </tr>
                    <tr>
                        <td height="24" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><b><font size=4 color="#3B3838">Results</font></b></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                        <td align="left" valign=bottom><font color="#000000"><br></font></td>
                    </tr>
                   
                    
                </table>
                <table border="0" cellpadding="5" cellspacing="0">
                    <!-- ***********************************************************************************************************Table ************************************************************* -->
                    <thead>
                        <td height="19" align="left" valign=bottom><font color="#000000"><br></font></td>
                        <th align="left" valign=bottom bgcolor="#404040"><b><font color="#FFFFFF">Adverse Effect</font></b></td>
                        <th align="left" valign=bottom bgcolor="#404040"><b><font color="#FFFFFF">Parameter</font></b></td>
                        <th align="left" valign=bottom bgcolor="#404040"><b><font color="#FFFFFF">Value</font></b></td>
                        <th align="left" valign=bottom bgcolor="#404040"><b><font color="#FFFFFF">Risk category</font></b></td>
                        <th colspan=2 align="left" valign=bottom bgcolor="#404040"><b><font color="#FFFFFF"><span>Description</span></font></b></td>
                        <th colspan=2 align="left" valign=bottom bgcolor="#404040"><b><font color="#FFFFFF"><span>Options for Consideration</span></font></b></td>
                    </thead>
                    {self.results()}
                <!-- ***********************************************************************************************************Results************************************************************* -->

                </table>  
                </body>

                </html>

        
        """
        return html