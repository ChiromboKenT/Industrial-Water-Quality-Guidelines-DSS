#--------------------------------------------------------------------------------------------------------Calculations----------------------------------------------------------

import math
def Bicarbonate(pAlkalinity, tAlkalinity):
    bCarb = 0
    if(pAlkalinity == 0):
        bCarb = tAlkalinity
    elif(pAlkalinity == tAlkalinity ):
        bCarb = 0       #J5
    elif(2 * pAlkalinity == tAlkalinity):
        bCarb = 0       #J6
    elif(2 * pAlkalinity < tAlkalinity):
        bCarb = (tAlkalinity - 2* pAlkalinity) if (pAlkalinity > 0) else 0  #J7
    elif(2 * pAlkalinity > tAlkalinity):
        bCarb = 0       #J8
    else :
        bCarb = 0 

    return bCarb
def Carbonate(pAlkalinity, tAlkalinity):
    carb = 0
    if(pAlkalinity == 0):
        carb = 0
    elif(pAlkalinity == tAlkalinity ):
        carb = 0       #I5
    elif(2 * pAlkalinity == tAlkalinity):
        carb = 2 * pAlkalinity #I6
    elif(2 * pAlkalinity < tAlkalinity):
        carb = 2 * pAlkalinity if (pAlkalinity > 0) else 0      #i7
    elif(2* pAlkalinity > tAlkalinity):
        carb = 2 * (tAlkalinity - pAlkalinity)
    else:
        carb = 0
    return carb
def Aggressive(inputs):
    TotalHardness = (inputs["Calcium"] * 2.5) + (inputs["Magnesium"] *4.1)
    carbonate = Carbonate(inputs['P Alkalinity'], inputs['Alkalinity'])
    bicarbonate = Bicarbonate(inputs["P Alkalinity"], inputs["Alkalinity"])

    alkalinity = (bicarbonate * 50.04/61.008) + (2 * carbonate * (50.04/61.008))

    print(f"Carbonate: {carbonate}")
    print(f"Bicarbonate: {bicarbonate}")
    print(f'Alkalinity: {alkalinity}')
    print(f'Hardness: {TotalHardness}')
    temp = TotalHardness * alkalinity
    aggressive = inputs["pH"] + math.log(temp, 10)
    return aggressive
def Langelier(inputs):
    CalciumHardness = inputs['Calcium'] / 0.401
    A = (math.log((inputs['Total Dissolved Solids']),10) -1) / 10
    B = (-13.12) *math.log((inputs["Temperature"] +273.2), 10) + 34.55
    C = math.log(CalciumHardness,10) - 0.4
    D = math.log(inputs['Alkalinity'],10)  #needs to be investigated
    
    print(f"Langlier A:{A}")
    print(f"Langlier B:{B}")
    print(f"Langlier C:{C}")
    print(f"Langlier D:{D}")
    phs = (9.3 + A + B) - (C + D) 
    print(f"Langlier phs{phs}")
    langelier = inputs["pH"] - phs
    print(f"Langlier : {langelier}")
    return langelier    
def rsiAtTemp(temp, inputs):
    CalciumHardness = inputs['Calcium'] / (40.08/2)
    TotalHardness = (inputs["Calcium"] * 2.5) + (inputs["Magnesium"] *4.1) 
    rsi = (
        2 * (
                11.017 + 0.197* math.log(abs(inputs['Total Dissolved Solids'] +1), 10)
                - 0.995 * math.log(abs((CalciumHardness * 0.4) - 1), 10)
                - 0.016 * math.log(abs((TotalHardness - CalciumHardness)* 0.24 + 1)) 
                - 1.041 * math.log(abs(inputs["Alkalinity"] - 1), 10)
                + 0.021 * math.log(abs(inputs["Sulphate"] + 1), 10)
                - (temp * (9 / 5) + 32 - 77)/120.5
            ) - inputs["ph"]
    )
    return rsi
def Pisigan(inputs):
    CalciumHardness = inputs['Calcium'] / (40.08/2)
    #MagnesiumHardness = inputs["Magnesium"]/(24.32/2)
    #TotalHardness = (inputs["Calcium"] * 2.5) + (inputs["Magnesium"] *4.1) 
    langlier = Langelier(inputs)
    #rsi_40 = rsiAtTemp(40,inputs)
    #rsi_60 = rsiAtTemp(60, inputs)
    #rsi_80 = rsiAtTemp(80, inputs)
    #phs = rsiAtTemp(inputs["Temperature"], inputs)

    ea = inputs["Alkalinity"] / 50045.5
    i = inputs["Total Dissolved Solids"] /40000
    t = ts = inputs["Temperature"] + 273.15
    d = -7.047968 + 0.016796 * t + 1795.711/t - 0.0000141566*(t**2)-153541/(t**2)
    dw = 87.74-0.4008* inputs["Temperature"] + 0.0009398*(inputs["Temperature"]**2)+0.00000141*(inputs["Temperature"]**3)
    aa = 1824600*(d**0.5)/(dw*t)**1.5
    bb = 50.29*d**0.5/(dw*t)**0.5
    yc =(-aa*4*(i**0.5)/(1+(bb*5*(i**0.5)))+0.165*i)
    yr = - aa *4*(i**0.5)/(1+(bb*5.4*(i**0.5)))
    ya = -aa*1*(i**0.5)/(1+(bb*5.4*(i**0.5)))
    yh = -aa*1*(i**0.5)/(1+(bb*9*(i**0.5)))
    yx = -aa*1*(i**0.5)/(1+(bb*3.5*(i**0.5)))
    yu = -0.5 * i
    k1_a  = -356.3094-0.06091964*t+21834.37/t+126.8339*math.log(t,10)-1684915/(t**2)
    k2_a = -107.8871-0.03252849*t+5151.79/t+38.92561*math.log(t,10)-563713.9/(t**2)
    kw_a = 35.3944-0.00853*t-5242.39/t-11.8261*math.log(t,10)

    k1_b = 10**(k1_a+yu-yh-ya)
    k2_b = 10**(k2_a+ya-yh-yr)
    kw_b = 10**(kw_a-yh-yx)

    h =10**(-inputs["pH"]- yh)
    cd = h*h+k1_b*h+k1_b*k2_b
    r3 = k1_b * k2_b/cd
    oh = kw_b/h

    b1 =r3*h*((ea*h)+(h*h)-kw_b)
    b2 =(k1_b*h)+(2*k1_b*k2_b)
    b3 =(h/k2_b)+(k1_b/h)+4
    bi =2.303*((b1*b3/b2)+oh+h)*50045

    js =(inputs["Chloride"]**0.509)*(inputs["Sulphate"]**0.0249)*(inputs["Alkalinity"]**0.423)*(inputs["Dissolved Oxygen"]**0.799)
    rp = ((0.4*CalciumHardness)**0.676)*(bi**0.0304)*((10**langlier)**0.107)*(inputs['Days of Exposure']**0.382)

    corrosionRate = js/rp
    return corrosionRate
def Larson(inputs):
    chloride_ = inputs["Chloride"] /35.45
    sulphate_ = inputs["Sulphate"]/48.03

    bicarbonate = Bicarbonate(inputs['P Alkalinity'],inputs['Alkalinity'])/61
    carbonate = Carbonate(inputs['P Alkalinity'],inputs["Alkalinity"])/30

    #print(f"Larson cl-: {chloride_}")
    #print(f"Larson SO-: {sulphate_}")
    #print(f"Larson HCO-: {carbonate}")
    #print(f"Larson CO3-: {bicarbonate}")
    larson = (chloride_ + sulphate_ )/(bicarbonate + carbonate)

    return larson
def Ryznar(inputs):
    tempCalcium = (inputs["Calcium"] * 10) / 4.01
    print("Temp Calcium:{}".format(tempCalcium))
    A = (math.log((inputs['Total Dissolved Solids']),10)-1) / 10
    print("A:{}".format(A))
    B = (-13.12) *math.log((inputs["Temperature"] +273.2), 10) + 34.55
    print("B:{}".format(B))
    C = math.log(tempCalcium,10) - 0.4
    print("C:{}".format(C))
    D = math.log(inputs['Alkalinity'],10)  #needs to be investigated
    print("D:{}".format(D))
    phs = (9.3 + A + B) - (C + D)
    print("phs:{}".format(phs))
    ryznar = 2 * phs - inputs["pH"] 

    return ryznar
def calciumPhospahate(inputs):
    try:
        ph_a = inputs["pH"]
        CalciumHardness = inputs['Calcium'] / 0.401
        phosphateConcentration = inputs["Phosphate"]
        temp = inputs["Temperature"]
        ph_c = (11.755 - math.log(CalciumHardness,10) - math.log(phosphateConcentration,10) - (2 * math.log(temp,10)))  / 0.65
        SI = ph_a - ph_c
        return SI
    except Exception as e:
        print(f'Calcium Phosphate Calculation Error: {e}') 


def Analyze(material,assesments,inputs):
    data = {}
    print(f"Inputs : {inputs}")
    if(material == "Stainless steel 304/304L" or material == "Stainless steel 316/316L" or 
        material == "Stainless steel Alloy 20" or material == "Stainless steel 904L" or material == "Duplex Stainless Steel" ):

        
        for assessment in assesments:
            try:
                if(assessment == "Corrosion" or assessment == "Scaling"):
                #calculate Ryznar
                    data['ryznar'] = Ryznar(inputs)
                    print("General Corrosion: {}".format(data['ryznar']))
                    data["Langlier"] = Langelier(inputs)
                if(assessment == "Corrosion"):
                    #Calclulate Flouride
                    data["Flouride"] = inputs["Flouride"]
                    #Calclualte Chloride
                    data["Chloride"] = inputs["Chloride"]
                    #Calculate Temperature
                    data["Temperature"] = inputs["Temperature"]
                    #Calculate pH
                    data["pH"] = inputs["pH"]
                    if(material == "Stainless steel 316/316L"):
                        data["Critical Pitting Temp"] = 18
                        data["PREN"] = 20
                    elif(material == "Stainless steel 316/316L"):
                        data["Critical Pitting Temp"] = 20
                        data["PREN"] = 25
                    elif(material == "Stainless steel Alloy 20"):
                        data["Critical Pitting Temp"] = 90
                        data["PREN"] = 30
                    elif(material == "Stainless steel 904L"):
                        data["Critical Pitting Temp"] = 40
                        data["PREN"] = 36
                    elif(material == "Duplex Stainless Steel"):
                        data["Critical Pitting Temp"] = 65
                        data["PREN"] = 46    
                elif(assessment == "Scaling"):
                    #Calculate Silica in steam
                    if(inputs["Silica in steam"] > 1):
                        data["Silica Concentration in steam"] = inputs["Silica in steam"]
                    #Calculate pH, Magnesium and Silica 
                    data["pH"] = inputs["pH"]
                    if(inputs["Silica"]):
                        data["SilicaMagnesium"] = inputs["Silica"] * inputs["Magnesium"]
                    #Water Treatment, Ca * S0$
                    ##data["WaterTreatment"] = inputs["WaterTreatment"]
                    data['WaterTreatment'] = inputs["Contains Antiscalants?"]
                    
                    data["CalciumSulphate"] = inputs["Calcium"] * inputs["Sulphate"]
                    data["CalciumPhosphate"] = calciumPhospahate(inputs)
                elif(assessment == "Fouling"):
                    #Calculate Suspended solids
                    data["Suspended Solids"] = inputs["Suspended Solids"]
                    print( data["Suspended Solids"])
            except Exception as e:
                print(f"Stainless Steal Calculation Error: {e}")
                continue
    elif(material == "Carbon Steel"):
        for assessment in assesments:
            try:
                if(assessment == "Corrosion" or assessment == "Scaling"):
                    #calculate Ryznar
                    data['ryznar'] = Ryznar(inputs)
                    print("General Corrosion: {}".format(data['ryznar']))
                    data["Langlier"] = Langelier(inputs)
                if(assessment == "Corrosion"):
                    #Larson Scold Index
                    data['larson'] = Larson(inputs)
                    print(f'Larson Index: {data["larson"]}')
                    #pisigan and Shingley Index & Corrosion Rate
                    data["pisigan corrosion"] = Pisigan(inputs) 
                    #If Open or Closed Reticulation
                    data["reticulation"] = inputs["Open reticulation system?"]

                    print(f'Pisigan Index:{ data["pisigan corrosion"]}')
                elif(assessment == "Scaling"):
                    #Calculate Silica in steam
                    if(inputs["Silica in steam"] > 1):
                        data["Silica Concentration in steam"] = inputs["Silica in steam"]
                    data["pH"] = inputs["pH"]
                    if(inputs["Silica"]):
                        data["SilicaMagnesium"] = inputs["Silica"] * inputs["Magnesium"]
                    #Water Treatment, Ca * S0$
                    #data["WaterTreatment"] = inputs["WaterTreatment"]
                    data['WaterTreatment'] = inputs["Contains Antiscalants?"]
                    data["CalciumSulphate"] = inputs["Calcium"] * inputs["Sulphate"]
                    data["CalciumPhosphate"] = calciumPhospahate(inputs)

                    print(" Calcium Sulpahate: {}...".format(data["CalciumSulphate"]))
                elif(assessment == "Fouling"):
                    #Calculate Suspended solids
                    data["Suspended Solids"] = inputs["Suspended Solids"]
                    print( data["Suspended Solids"])
            except Exception as e:
                print(f'Carbon Steel Calculation error: {e}')
                
    elif(material == "Concrete"):
        for assessment in assesments:
            try:
                if(assessment == "Corrosion" or assessment == "Scaling"):
                    #calculate Ryznar
                    data['ryznar'] = Ryznar(inputs)
                    print("General Corrosion: {}".format(data['ryznar']))
                    data["Langlier"] = Langelier(inputs)
                if(assessment == "Corrosion"):
                    #Calculate Aggressive Index
                    data["Aggressive"] = Aggressive(inputs)
                    #IsConcrete Reinforced
                    data["Concrete Reinforced"] = inputs['Is the concrete reinforced?']
                    print(data["Aggressive"])
                elif(assessment == "Scaling"):
                    
                    #Calculate The Sulphate
                    data["Sulphate"] = inputs["Sulphate"]
                    print("Sulpahate Conc: {}...".format( data["Sulphate"]))
                elif(assessment == "Fouling"):
                    #Calculate Suspended solids
                    data["Suspended Solids"] = inputs["Suspended Solids"]
                    print( data["Suspended Solids"])
            except Exception as e:
                print(f"Error !Concrete in Fouling,: {e}")
                continue
    elif(material == "Monel-Lead/Copper Alloys"):
        for assessment in assesments:
            try:
                if(assessment == "Corrosion" or assessment == "Scaling"):
                    #calculate Ryznar
                    data['ryznar'] = Ryznar(inputs)
                    print("General Corrosion: {}".format(data['ryznar']))
                    try:
                        data["Langlier"] = Langelier(inputs)
                    except Exception as e:
                        print(f"Langlier Calculation Error: {e}")
                if(assessment == "Corrosion"):
                    #Larson Skold Index
                    data['larson'] = Larson(inputs)
                    print(data["larson"])
                    #Chloride to Sulphate Mass Ratio
                    data["csmr"] = inputs['Chloride'] / inputs["Sulphate"]
                    #PREN
                    #Does material Contain lead or copper
                    data["Lead or Copper"] = True if (inputs["Does Material contain Lead?"] or inputs["Does Material contain Copper?"]) else False

                    print(data["csmr"])
                elif(assessment == "Scaling"):
                    #Calculate Silica in boiler steam
                    if(inputs["Silica in steam"] > 1):
                        data["Silica Concentration in steam"] = inputs["Silica in steam"]
                    #Calculate pH, Magnesium and Silica 
                    
                    data["pH"] = inputs["pH"]
                    try:
                        data["SilicaMagnesium"] = inputs["Silica"] * inputs["Magnesium"]
                    except Exception as e:
                        print(f'Alloy Error Silica Magnesium: {e}')
                    #Water Treatment, Ca * S0$
                    #data["WaterTreatment"] = inputs["WaterTreatment"]
                    data['WaterTreatment'] = inputs["Contains Antiscalants?"]
                    data["CalciumPhosphate"] = calciumPhospahate(inputs)
                    try:
                        
                        data["CalciumSulphate"] = inputs["Calcium"] * inputs["Sulphate"]
                    except Exception as e:
                        print("Alloy Error Calcium: {e}")
                elif(assessment == "Fouling"):
                    #Calculate Suspended solids
                    data["Suspended Solids"] = inputs["Suspended Solids"]
                    print( data["Suspended Solids"])
            except Exception as e:
                print(f"Alloy calculation error: {e}")
                continue
    elif(material == "Plastic"):
        for assessment in assesments:
            try:
                if(assessment == "Scaling"):
                    #Calculate General Corrosion
                    data['ryznar'] = Ryznar(inputs)
                    data["CalciumPhosphate"] = calciumPhospahate(inputs)
                    print("General Corrosion: {}".format(data['ryznar']))
                elif(assessment == "Fouling"):
                    #Suspended Solids
                    data["Suspended Solids"] = inputs["Suspended Solids"]
                    print( data["Suspended Solids"])
            except Exception as e:
                print(f"Plastic Caclution error: {e}")

    elif(material == "Membranes"):
        for assessment in assesments:
            try:
                if(assessment == "Corrosion" or assessment == "Scaling"):
                    try:
                        data["Langlier"] = Langelier(inputs)
                    except Exception as e:
                        print(f"Langlier Calculation Error: {e}")
                if(assessment == "Scaling"):
                    data["CalciumPhosphate"] = calciumPhospahate(inputs)
                elif(assessment == "Fouling"):
                    #Silt Index Sensity
                    try:
                        if(inputs["Silt Density Index"] > 0):
                            data["Silt Density Index"] = inputs["Silt Density Index"]
                    except KeyError as k:
                        print("Error Silt Density")
                        
                    #Particle Size
                    try:
                        if(inputs["Particle Size"] > 0):
                            data["Particle Size"] = inputs["Particle Size"]
                            data["Technology Type"] = inputs['Technology Type']
                    except KeyError as k:
                        print(f"Particle Size key error: {k}")
                        
                    #Suspended Solids
                    data["Suspended Solids"] = inputs["Suspended Solids"]
                    print( data["Suspended Solids"])
            except Exception as e:
                print(f"Error Membranes Calculation: {e}")
                continue
    print(f'Calucalted Data: {data}')
    return data
