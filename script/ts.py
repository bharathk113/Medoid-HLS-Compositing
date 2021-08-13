import gdal,glob,os,math,numpy
"""
HLS Band Code Name L30	HLS Band Code Name S30	HLS L30 hdf	      HLS S30 hdf	Wavelength (micrometers)	Band
band01	                 B01	                    0	              0	          0.43 – 0.45	           Coastal Aerosol
band02	                 B02	                    1	              1	          0.45 – 0.51	           Blue
band03	                 B03	                    2	              2	          0.53 – 0.59	           Green
band04	                 B04	                    3	              3	          0.64 – 0.67	           Red
-	                     B05	                    -	              4	          0.69 – 0.71	           Red-Edge 1
-	                     B06	                    -	              5	          0.73 – 0.75	           Red-Edge 2
-	                     B07	                    -	              6	          0.77 – 0.79	           Red-Edge 3
-	                     B08	                    -	              7	          0.78 – 0.88	           NIR Broad
band05	                 B8A	                    4	              8   	      0.85 – 0.88	           NIR Narrow
band06	                 B11	                    5	              11	      1.57 – 1.65	           SWIR 1
band07	                 B12	                    6	              12	      2.11 – 2.29	           SWIR 2
-	                     B09	                    -	              9	          0.93 – 0.95	           Water Vapor
band09	                 B10	                    7	              10	      1.36 – 1.38	           Cirrus
band10	                 -	                        8	              -	          10.60 – 11.19	           Thermal Infrared 1
band11	                 -	                        9	              -	          11.50 – 12.51	           Thermal Infrared 2
            s2-13 qa
            l8-10 qa

"""
"""
Function to check data and prepare the QA masks
"""
def checkdata(imagesList,noDataVal):
    X,Y=[[],[]]
    noDataMasks=[]
    for eachImage in imagesList:
        raster=gdal.Open(eachImage)
        for i in range(len(raster.GetSubDatasets())):
            band=gdal.Open(raster.GetSubDatasets()[i][0])
            X.append(band.RasterXSize)
            Y.append(band.RasterYSize)
        if len(raster.GetSubDatasets())>12:
            band=gdal.Open(raster.GetSubDatasets()[13][0])
            # print(raster.GetNoDataValue())
        else:
            band=gdal.Open(raster.GetSubDatasets()[10][0])
            # print(raster.GetNoDataValue())
        QAarray=band.ReadAsArray()
        QAtags=createQABands(QAarray,noDataVal)
        print (eachImage)
        noDataMask=numpy.where(QAtags[0]==1,QAtags[0],numpy.where(QAtags[1],QAtags[1],numpy.where(QAtags[3],QAtags[3],0)))
        # print(eachImage,noDataMask)
        noDataMasks.append(noDataMask.astype(dtype=bool))
        # GT=band.GetGeoTransform()
        # prj=band.GetProjection()
        # driver = gdal.GetDriverByName('GTiff')
        # ds_out = driver.Create(os.path.join(r"D:\Projects\TimeSeries_Aug2021_01\outs",os.path.split(eachImage)[1][:-4]+'_nodata.tif'), band.RasterXSize, band.RasterYSize, 1, gdal.GDT_Byte, ['NBITS=1'])
        # ds_out.SetGeoTransform(GT)
        # ds_out.SetProjection(prj)
        # outBand=ds_out.GetRasterBand(1)
        # outBand.WriteArray(noDataMask)
        # for k in range(len(QAtags)):
        #     ds_out = driver.Create(os.path.join(r"D:\Projects\TimeSeries_Aug2021_01\outs",os.path.split(eachImage)[1][:-4]+str(k)+'.tif'), band.RasterXSize, band.RasterYSize, 1, gdal.GDT_Byte, ['NBITS=1'])
        #     ds_out.SetGeoTransform(GT)
        #     ds_out.SetProjection(prj)
        #     outBand=ds_out.GetRasterBand(1)
        #     outBand.WriteArray(QAtags[k])

    GT=band.GetGeoTransform()
    prj=band.GetProjection()
    # os.sys.exit()
    return(set(X),set(Y),GT,prj,noDataMasks)
"""
Function to prepare and stack images to form N-Dimesional arrays(39Images*7Bands*Xpixels*Ypixels) (from images) using the input data
"""
def makendArray(imagesList,numChunks,X,Y,chunkid,noDataMasks):
    ndArr=[]
    ndMask=[]
    L8Bands=[0,1,2,3,4,5,6]
    S2Bands=[0,1,2,3,8,11,12]
    readXPixels=int(math.floor(X/numChunks))
    readYPixels=int(math.floor(Y/numChunks))
    readXstart=readXPixels*chunkid[0]
    readYstart=readYPixels*chunkid[1]
    if chunkid[0]!=numChunks and chunkid[1]!=numChunks:
        for i in range(len(imagesList)):
        # for eachImage in imagesList:
            eachImage=imagesList[i]
            imageBands=[]
            raster=gdal.Open(eachImage)
            numBands=len(raster.GetSubDatasets())
            if numBands <12:
                for bno in L8Bands:
                    band=gdal.Open(raster.GetSubDatasets()[bno][0])
                    imageBands.append(band.ReadAsArray(readXstart,readYstart,readXPixels,readYPixels))
            else:
                for bno in S2Bands:
                    band=gdal.Open(raster.GetSubDatasets()[bno][0])
                    imageBands.append(band.ReadAsArray(readXstart,readYstart,readXPixels,readYPixels))
            # numBands=6
            # for i in range(numBands):
            #     band=gdal.Open(raster.GetSubDatasets()[i][0])
            #     imageBands.append(band.ReadAsArray(readXstart,readYstart,readXPixels,readYPixels))
            ndMask.append(noDataMasks[i][readYstart:readYstart+readYPixels,readXstart:readXPixels+readXstart])
            ndArr.append(imageBands)
    elif chunkid[0]==numChunks and chunkid[1]!=numChunks:
        for i in range(len(imagesList)):
        # for eachImage in imagesList:
            eachImage=imagesList[i]
            imageBands=[]
            raster=gdal.Open(eachImage)
            numBands=len(raster.GetSubDatasets())
            readXPixels=band.RasterXSize-(chunkid[0]*readXstart)
            if numBands <12:
                for bno in L8Bands:
                    band=gdal.Open(raster.GetSubDatasets()[bno][0])
                    imageBands.append(band.ReadAsArray(readXstart,readYstart,readXPixels,readYPixels))

            else:
                for bno in S2Bands:
                    band=gdal.Open(raster.GetSubDatasets()[bno][0])
                    imageBands.append(band.ReadAsArray(readXstart,readYstart,readXPixels,readYPixels))
            # numBands=6
            # for i in range(numBands):
            #     band=gdal.Open(raster.GetSubDatasets()[i][0])
            #     readXPixels=band.RasterXSize-(chunkid[0]*readXstart)
            #     imageBands.append(band.ReadAsArray(readXstart,readYstart,readXPixels,readYPixels))
            ndMask.append(noDataMasks[i][readYstart:readYstart+readYPixels,readXstart:readXPixels+readXstart])
            ndArr.append(imageBands)
    elif chunkid[0]!=numChunks and chunkid[1]==numChunks:
        for i in range(len(imagesList)):
        # for eachImage in imagesList:
            eachImage=imagesList[i]
            imageBands=[]
            raster=gdal.Open(eachImage)
            numBands=len(raster.GetSubDatasets())
            readYPixels=band.RasterYSize-(chunkid[1]*readYstart)
            if numBands <12:
                for bno in L8Bands:
                    band=gdal.Open(raster.GetSubDatasets()[bno][0])
                    imageBands.append(band.ReadAsArray(readXstart,readYstart,readXPixels,readYPixels))

            else:
                for bno in S2Bands:
                    band=gdal.Open(raster.GetSubDatasets()[bno][0])
                    imageBands.append(band.ReadAsArray(readXstart,readYstart,readXPixels,readYPixels))
            # numBands=6
            # for i in range(numBands):
            #     band=gdal.Open(raster.GetSubDatasets()[i][0])
            #     readYPixels=band.RasterYSize-(chunkid[1]*readYstart)
            #     imageBands.append(band.ReadAsArray(readXstart,readYstart,readXPixels,readYPixels))
            ndMask.append(noDataMasks[i][readYstart:readYstart+readYPixels,readXstart:readXPixels+readXstart])
            ndArr.append(imageBands)
    elif chunkid[0]==numChunks and chunkid[1]==numChunks:
        for i in range(len(imagesList)):
        # for eachImage in imagesList:
            eachImage=imagesList[i]
            imageBands=[]
            raster=gdal.Open(eachImage)
            numBands=len(raster.GetSubDatasets())
            readXPixels=band.RasterXSize-(chunkid[0]*readXstart)
            readYPixels=band.RasterYSize-(chunkid[1]*readYstart)
            if numBands <12:
                for bno in L8Bands:
                    band=gdal.Open(raster.GetSubDatasets()[bno][0])
                    imageBands.append(band.ReadAsArray(readXstart,readYstart,readXPixels,readYPixels))

            else:
                for bno in S2Bands:
                    band=gdal.Open(raster.GetSubDatasets()[bno][0])
                    imageBands.append(band.ReadAsArray(readXstart,readYstart,readXPixels,readYPixels))
            # numBands=6
            # for i in range(numBands):
            #     band=gdal.Open(raster.GetSubDatasets()[i][0])
            #     readXPixels=band.RasterXSize-(chunkid[0]*readXstart)
            #     readYPixels=band.RasterYSize-(chunkid[1]*readYstart)
            #     imageBands.append(band.ReadAsArray(readXstart,readYstart,readXPixels,readYPixels))
            ndMask.append(noDataMasks[i][readYstart:readYstart+readYPixels,readXstart:readXPixels+readXstart])
            ndArr.append(imageBands)
    return(ndArr,ndMask)
"""
Function to calculate N-Dimensional euclidean distance from the N-D arrays
"""
def distMat(ndArr,ndmask,noDataVal):
    D=[[numpy.full(numpy.array(ndArr[0][0]).shape,0,dtype=numpy.double) for i in range(len(ndArr))] for j in range(len(ndArr))]
    for i in range(0,len(ndArr)):
        for j in range(i,len(ndArr)):
            mask=numpy.where(ndmask[i]==1,ndmask[i],ndmask[j])
            arr1=numpy.array(ndArr[i],dtype=numpy.double)/10000
            arr1=numpy.where(arr1==noDataVal/10000,numpy.nan,arr1)
            arr2=numpy.array(ndArr[j],dtype=numpy.double)/10000
            arr2=numpy.where(arr2==noDataVal/10000,numpy.nan,arr2)
            D[i][j]=numpy.sqrt(numpy.sum((arr1-arr2)*(arr1-arr2),axis=0))

            D[i][j][mask]=numpy.nan
            D[j][i] = D[i][j]
    return (D)
"""
Function to generate medoid value for all the pixels
"""
def genMedArr(ndArr,ndMask,noDataVal):
    D=numpy.array(distMat(ndArr,ndMask,noDataVal))
    def Dsum(D):
        sumD=[]
        for i in range(len(D)):
            addArr=numpy.nansum(D[i],axis=0)

            addArr[numpy.all(numpy.isnan(D[i]),axis=0)] = numpy.nan
            sumD.append(addArr)
        return sumD
    sumD=numpy.array(Dsum(D))
    def createMed(sumD,ndArr):
        numRasters=sumD.shape[0]
        sumDX=sumD.shape[1]
        sumDY=sumD.shape[2]
        numBands=ndArr.shape[1]
        medArr=numpy.full((numBands,sumDX,sumDY),numpy.nan,numpy.double)
        for i in range(sumDX):
            for j in range(sumDY):
                if numpy.isnan(sumD[:,i,j]).all():
                    medArr[:,i,j]=numpy.array([numpy.nan for k in range(ndArr[0,:,i,j].shape[0])])
                else:
                    index=numpy.nanargmin(sumD[:,i,j])
                    medArr[:,i,j]=ndArr[index,:,i,j]
        return (medArr,sumDY, sumDX, numBands)
    medArr,sumDY, sumDX, numBands=createMed(sumD,numpy.array(ndArr))
    return (medArr,sumDY, sumDX, numBands)
"""
Function to obtain the QA tags
"""
def createQABands(QAband,noDataVal):
    QAband=numpy.where(QAband==noDataVal,0,QAband)
    cirrus=QAband%2==1
    cloud=(numpy.floor(QAband/2))%2==1
    cloudAdj=(numpy.floor(QAband/4))%2==1
    shadow=(numpy.floor(QAband/8))%2==1
    snow=(numpy.floor(QAband/16))%2==1
    water=(numpy.floor(QAband/32))%2==1
    return(cirrus,cloud,cloudAdj,shadow,snow,water)
"""
main function
"""
def main():
    imagesList=glob.glob(r"..\subset\*.hdf")
    if len(imagesList)<1:
        print("No datasets are found. Please check the input data location")
        os.sys.exit()
    numChunks=10
    noDataVal=-1000
    noDataValQA=255
    XDims,YDims,GT,prj,noDataMasks=checkdata(imagesList,noDataValQA)
    if len(XDims)!=1 or len(YDims)!=1:
        print("Inconsistency found in input data. Please check..")
        os.sys.exit()
    X,Y=[list(XDims)[0],list(YDims)[0]]
    driver = gdal.GetDriverByName('GTiff')
    ds_out = driver.Create(r"..\outs\test.tif", X, Y, 7, gdal.GDT_Float32)
    ds_out.SetGeoTransform(GT)
    ds_out.SetProjection(prj)
    for i in range(0, numChunks):
        for j in range(0, numChunks):
            print ("Please wait while chunk id",i,j,"is being loaded")
            ndArr,ndMask=makendArray(imagesList,numChunks,X,Y,(i,j),noDataMasks)
            print ("Chunk",i,j, "is loaded. Calculating medoid..")
            medArr,sumDY, sumDX, numBands = genMedArr(ndArr,ndMask,noDataVal)
            for k in range(1,numBands+1):
                outband=ds_out.GetRasterBand(k)
                outband.WriteArray(medArr[k-1],i*math.floor(X/numChunks),j*math.floor(Y/numChunks))
                outband.FlushCache()
                ds_out.FlushCache()


if __name__=="__main__":
    main()
