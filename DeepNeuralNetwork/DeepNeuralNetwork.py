#Import the native app object.
from native import app
#from wadmissiondataset import admission_data
from dnn import DeepNeuralNetwork
import deepmath as dm
import random, json, time, os, ast
from datetime import datetime

#Called when application is created.
def OnStart():
    global lay, lst, spin, tv0, tv3,  tvEpoch, tvExpected, tvPredicted, tvError, tvDataset, addDataDialog, edData, edHiddenLayer, edModelName, edEpoch, modelDialog, addDataDialog, chkTrainData, chkPredictData, spinAddData
    #Create a layout with objects vertically centered.
    app.ShowProgress( "" )
    lay = app.CreateLayout( "linear", "VCenter,FillXY" )
    app.MakeFolder( "/sdcard/aidata" )
    #app.WriteFile( "/sdcard/aidata/xor/dataset.json", " [[[0, 0], [0, 0]],[[0, 1], [1, 1]],[[1, 0], [1, 1]],[[1, 1], [0, 0]]]" )
    
    #Add a button 30% of screen width.
    btnAddData = app.AddButton( lay, "Add Data", 0.3 )
    btnAddData.SetMargins( 0, 0.02, 0, 0 )
    btnAddData.SetOnTouch( btnAddData_OnTouch )
    
    btnDeleteData = app.AddButton( lay, "Delete Data", 0.3 )
    btnDeleteData.SetMargins( 0, 0.02, 0, 0 )
    btnDeleteData.SetOnTouch( btnDeleteData_OnTouch )
    
    btnPredict = app.AddButton( lay, "Predict", 0.3 )
    btnPredict.SetMargins( 0, 0.02, 0, 0 )
    btnPredict.SetOnTouch( btnPredict_OnTouch )
    
    btnTrain = app.AddButton( lay, "Train", 0.3 )
    btnTrain.SetMargins( 0, 0.02, 0, 0 )
    btnTrain.SetOnTouch( btnTrain_OnTouch )
    
    tv0= app.AddText( lay, "="*30 )
    tv0.SetMargins( 0, 0.04, 0, 0 )
    tv3= app.AddText( lay, "=", 1, -1, "Multiline" )
    tv3.SetMargins( 0, 0.00, 0, 0 )
    tv3.SetTextColor( "#22ff22" )
    tv1= app.AddText( lay, "="*30 )
    tv1.SetMargins( 0, 0.00, 0, 0 )
    tvEpoch = app.AddText( lay, "" )
    tvEpoch.SetTextColor("#00FFFF")
    tvEpoch.SetMargins( 0, 0.02, 0, 0 )
    tvExpected = app.AddText( lay, "" )
    tvExpected.SetTextColor( "#22ff22" )
    tvExpected.SetMargins( 0, 0.02, 0, 0 )
    tvPredicted= app.AddText( lay, "" )
    tvPredicted.SetTextColor("#FFFF00");
    tvPredicted.SetMargins( 0, 0.02, 0, 0 )
    tvError= app.AddText( lay, "" )
    tvError.SetTextColor("#FF0000");
    tvError.SetMargins( 0, 0.02, 0, 0 )
    tv2= app.AddText( lay, "="*30 )
    tv2.SetMargins( 0, 0.02, 0, 0 )
    
    #lst = app.ListFolder( "/sdcard/weights", ".txt" )
    #spin = app.AddSpinner( lay, lst )
    #spin.SetMargins( 0.0, 0.03, 0.00, 0.00 )
    #app.CreateList( lst, 1, -1 )
    #app.AddList( lay, lst )
    
    #DIALOG ADD DATA
    addDataDialog = app.CreateDialog( "ADD DATA" )
    layAddData = app.CreateLayout( "linear", "VTop,FillXY" )
    layAddData.SetSize( 0.8, -1);
    
    btnChooseData= app.AddButton( layAddData, "CHOOSE DATASET '.txt'", 0.3 )
    btnChooseData.SetMargins( 0, 0.02, 0, 0 )
    btnChooseData.SetOnTouch( btnChooseData_OnTouch )
    
    tvDataset = app.AddText( layAddData, "" )
    tvDataset.SetTextColor( "#22ff22" )
    
    chkTrainData = app.AddCheckBox( layAddData, "TRAIN DATASET" )
    chkTrainData.SetChecked( True)
    chkTrainData.SetOnTouch( chkTrainData_OnTouch )
    chkPredictData = app.AddCheckBox( layAddData, "PREDICT DATASET" )
    chkPredictData.SetChecked( False )
    chkPredictData.SetOnTouch( chkPredictData_OnTouch )
    
    spinAddData = app.AddSpinner( layAddData, "" )
    spinAddData.SetEnabled( False )
    
    edModelName = app.AddTextEdit( layAddData,"", 0.4, -1, "SingleLine")
    edModelName.SetHint( "MODEL_NAME" )
    edEpoch = app.AddTextEdit( layAddData,"", 0.4, -1, "SingleLine, Numbers")
    edEpoch.SetHint( "EPOCH = 1000" )
    edHiddenLayer= app.AddTextEdit( layAddData,"", 0.55, -1, "SingleLine")
    edHiddenLayer.SetHint( "HIDDEN-LAYER =  [5, 4, 5]" )
    
    btnSaveData= app.AddButton( layAddData, "SAVE DATA", 0.3 )
    btnSaveData.SetMargins( 0, 0.02, 0, 0 )
    btnSaveData.SetOnTouch( btnSaveData_OnTouch )
    
    
    
    
    #edData = app.AddTextEdit( layAddData,"", 0.75, -1)
    #edData.SetHint( "dataset = [ [[0, 1], [1]], \n[[1, 0], [1]], [[0, 0], [0]], [[1, 1], [0]] ]" )
    
    #layAddData.AddChild( btnSaveData )
    addDataDialog.AddLayout( layAddData )
    #Add layout to app.
    app.AddLayout( lay )
    app.HideProgress()
    
#ADD DATA BUTTON ON CLICK
def btnAddData_OnTouch():
       addDataDialog.Show()
 
#DELETE DATA BUTTON ONCLICK
def btnDeleteData_OnTouch():
       deleteDataDialog = app.CreateListDialog("DELETE DATA - CHOOSE MODEL ", app.ListFolder( "/sdcard/aidata" ))
       deleteDataDialog.SetOnTouch(deleteDataDialog_OnTouch)
       deleteDataDialog.Show()
       
def deleteDataDialog_OnTouch(item, index):
        app.ShowProgress( "DELETING FILE" )
        if item == "":
           app.ShowPopup( "DATA NOT FOUND." )
           app.HideProgress()
        else:
               app.DeleteFolder( "/sdcard/aidata/"+item )
               app.HideProgress()
               app.ShowPopup( "FILE DELETED SUCCESSFULY." )
        

def chkTrainData_OnTouch( isChecked ):
        chkTrainData.SetChecked( True ); chkPredictData.SetChecked( False )
        edModelName.SetEnabled( True ); edEpoch.SetEnabled( True); edHiddenLayer.SetEnabled( True )
        edModelName.SetText( "" ); edEpoch.SetText( "" ); edHiddenLayer.SetText( "" )
        spinAddData.SetEnabled( False)
        spinAddData.SetList( "" )       

def chkPredictData_OnTouch( isChecked ):
       chkTrainData.SetChecked( False); chkPredictData.SetChecked( True)
       edModelName.SetEnabled( False ); edEpoch.SetEnabled(False ); edHiddenLayer.SetEnabled( False )
       edModelName.SetText( " " ); edEpoch.SetText( " " ); edHiddenLayer.SetText( " " )
       spinAddData.SetEnabled( True )
       spinAddDataList = app.ListFolder( "/sdcard/aidata" )
       spinAddData.SetList( spinAddDataList)
               
#BUTTON CHOOSE DATA ONCLICK
def btnChooseData_OnTouch():
       app.ChooseFile( "Choose a File", "*/*", OnChoose )
    
def OnChoose( file ):
    app.ShowProgress( "LOADING DATA" )
    file_extension = os.path.splitext(file)[1]
    if file_extension == ".txt":
       try: 
            edData = ast.literal_eval(app.ReadFile( file ))
            tvDataset.SetText(file )
            app.ShowPopup( "FILE CHOSEN SUCCESSFULLY." )
            app.HideProgress()
       except: 
              app.ShowPopup( "THE CHOOSEN FILE CONTAIN A BAD FORMAT DATASET." )
              app.HideProgress()
    else:
            app.Alert(f"THIS APP DOESN'T SUPPORT THE EXTENSION: {file_extension}" )
            app.HideProgress()

            

#SAVE DATA BUTTON ON CLICK
def btnSaveData_OnTouch():
       if chkPredictData.GetChecked() == True:
          #app.ShowPopup( "Verdade "+spinAddData.GetText() )
           if tvDataset.GetText() == "":
                   app.ShowPopup( "CHOOSE THE DATASET FILE '.txt'" )
           else:
                  if spinAddData.GetText() == "":
                      app.ShowPopup( "~ THERE IS NO A MODEL SAVED YET. \n~ FIRST ADD TRAINING DATA." )
                  else:
                         path =  "/sdcard/aidata/"+spinAddData.GetText()
                         edData = ast.literal_eval(app.ReadFile( tvDataset.GetText() ))
                         if app.FileExists( path+"/predictdataset.json" ) == True:
                             app.DeleteFile( path+"/predictdataset.json")
                             app.ShowPopup( "File deleted to save a new one" )
                         else:
                                #app.ShowPopup( "File doesnt exist. a new one will be created." )
                                app.WriteFile( path+"/predictdataset.json", str(edData) )
                                tvDataset.SetText( "" )
                                app.ShowPopup( "PREDICT DATASET SAVED SUCCESSFULLY." )
                                addDataDialog.Dismiss()
                 
       else:
             if edModelName.GetText() == "" or edEpoch.GetText() == "" or edHiddenLayer.GetText() == "":
                app.ShowPopup( "FILL ALL THE BLANK SPACE." )
             else:
                   if tvDataset.GetText() == "":
                       app.ShowPopup( "CHOOSE THE DATASET FILE '.txt'" )
                   else:
                         edData = ast.literal_eval(app.ReadFile( tvDataset.GetText() ))
                         lstFolder = app.ListFolder( "/sdcard/aidata" ) 
                         if edModelName.GetText().lower() in lstFolder:
                            app.ShowPopup( "~ THE MODEL: '"+edModelName.GetText()+"' ALREADY EXIST." )
                         else:
                               path =  "/sdcard/aidata/"+edModelName.GetText().lower() 
                               app.MakeFolder( path )
                               app.WriteFile( path+"/dataset.json", str(edData).replace(" ","").replace("  ","").replace("   ","") )
                               app.WriteFile( path+"/hidden.json", edHiddenLayer.GetText() )
                               app.WriteFile( path+"/epoch.json", edEpoch.GetText().replace(",","").replace(".","") )
                               app.ShowPopup( "~ THE MODEL:'"+edModelName.GetText()+"' SAVED SUCCESSFULY." )
                               edModelName.SetText( "" ); edEpoch.SetText( "" )
                               edHiddenLayer.SetText( "" ); tvDataset.SetText( "" )
                               app.ShowPopup( "~ TRAIN DATASET SAVED SUCCESSFULLY." )
                               addDataDialog.Dismiss()
                               
                    
                 
    
                        
                                                
                                                                        
                                                                                                
                                                                                                                                                
#BUTTON PREDICT
#ONCLICK                        
def btnPredict_OnTouch():
       app.ShowProgress( "" )
       models = app.ListFolder("/sdcard/aidata")
       if not models:
          app.ShowPopup("~ NO MODEL FOUND. \n~ ADD A MODEL AND TRAIN IT FIRST.")
          app.HideProgress()
       else:
              app.HideProgress()
              modelDialog = app.CreateListDialog("CHOOSE MODEL FOR PREDICTION", models)
              modelDialog.SetOnTouch(predictModel_OnTouch)
              modelDialog.Show()
              
#ONDIALOG CHOOSE MODEL              
def predictModel_OnTouch(item, index):
       app.ShowProgress( "LOADING DATA" )
       path = "/sdcard/aidata/"+item+"/predictdataset.json"
       if app.FileExists( path ) == True:
           dnn = DeepNeuralNetwork( model_name = item )
           dataset = ast.literal_eval(app.ReadFile( path ))
           trainDataset = ast.literal_eval(app.ReadFile(  "/sdcard/aidata/"+item+"/dataset.json" ))
           
           try:
                if len(trainDataset[0][0]) == len(dataset[0]):
                   app.HideProgress()
                   for i in range(len(dataset)):
                         app.Alert( "DATASET: "+str(i+1)+"/"+str(len(dataset))+"\nDNN PREDICTED:"+str(dnn.feedforward(dataset[i])) )
                else:
                        app.HideProgress()
                        app.ShowPopup( "~ THE TRAIN INPUT DATASET DOESN'T MATCH WITH PREDICT DATASET." )
           except Exception as error:
                       app.ShowPopup( error )
       else:
              app.HideProgress()
              app.ShowPopup( f"~ PREDICT DATASET NOT FOUND FOR {item}. \n~ ADD PREDICT DATASET FIRST." )










#BUTTON TRAIN
#ONCLICK
def btnTrain_OnTouch():
        lst = app.ListFolder( "/sdcard/aidata")
        if lst == []:
            app.ShowPopup( "~ DATA NOT FOUND. CLICK 'Add Data' TO ADD DATA." )
        else:
             trainModelDialog = app.CreateListDialog( "CHOOSE MODEL FOR TRAIN", lst )
             trainModelDialog.SetOnTouch( trainModelDialog_OnTouch )
             trainModelDialog.Show()

##ONDIALOG CHHOSE MODEL        
def trainModelDialog_OnTouch(item, index):
       app.ShowProgress( "" )
       dnn = DeepNeuralNetwork( model_name = item )
       path = dnn.path
        
       tv3.SetText( item.upper()+".dnn\n"+"[ DATASET:["+str(len(dnn.dataset))+"] ]   "+"[ INPUT:"+str(dnn.input_nodes)+"  HIDDEN:"+str(dnn.hidden_nodes)+"  OUTPUT:"+str(dnn.output_nodes)+" ]" )
       epoch = int(app.ReadFile( path+"/epoch.json" ))
       for ep in range(epoch+1):
              data = random.choice(dnn.dataset)
              result = dnn.backPropagation(inputs = data[0], targets = data[1], learning_rate = 0.10)
              
              tvEpoch.SetText( "EPOCH: "+str(ep)+"/"+str(epoch)  )
              tvExpected.SetText( "EXPECTED: "+str(data[1])  )
              tvPredicted.SetText( "PREDICTED: "+str(result[0])  )
              tvError.SetText( "ERROR: "+str(result[2])  )
              
       app.HideProgress()     
       exists = app.FileExists( path )
       lstFiles = app.ListFolder( path, ".txt" )
       try:
            for f in lstFiles:
                  if app.FileExists( path+"/"+f ) == True:
                     app.DeleteFile( path+"/"+f )
                     #app.ShowPopup(path+"/"+f  )
       except Exception as error:
                     pass
       app.WriteFile( path+"/weights.txt", str(result[6]) )
       app.WriteFile( path+"/biases.txt", str(result[7]) )
       app.HideProgress()
       
       
       try:
           for i in range(len(dnn.dataset)):
                 app.Alert( "Expected:"+str(dnn.dataset[i][1])+"\nPredicted:"+str(dnn.feedforward(dnn.dataset[i][0])) )
       except:
                  pass
 
 
 
 
 




