


<!DOCTYPE html>
<html lang="en">
<head>

  <title>FindNearby</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="css/bootstrap.min.css">
  <link href="https://fonts.googleapis.com/css?family=Carter+One" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css?family=Marcellus" rel="stylesheet">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.2/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
  <script src="https://use.fontawesome.com/4ade0e5ef1.js"></script>
  <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCDmFqQa3GmRdYRtITKJnv3qF3-tsL5H2A&v=3.exp&sensor=false&libraries=places"></script>
  <script type="text/javascript">
               function initialize() {
                       var input = document.getElementById('diff_address');
                       var autocomplete = new google.maps.places.Autocomplete(input);
               }
               google.maps.event.addDomListener(window, 'load', initialize);
       </script>

  <style type="text/css">
    

     .navbar
     {    
      background-color: #121212;
      padding-right: 50px;
      padding-left: 50px;
      padding-bottom: 30px;
      padding-top:30px;
      color:white;
      height: 100px;
      text-align: center;
      font-family: 'Carter One', cursive;
      font-size: 20px;

     }

     .active
     {
      background-color: green;
     } 

     #lg_devices_foot
    {
      background-color: #121212;
      position:relative;
      padding: 10px;           
      height:50px;
      color: white;
      position: relative;
      right: 0;
      bottom: 0;
      left: 0;
    }
       #sm_devices_foot
    {

      background-color: #121212;
      
      color:white;

    }


        .fixedContainer
     {    
    position: fixed;    
    margin-left: 10px;    
    }


     


  </style>
 </head>

 <body>
  
  
  <nav class="navbar navbar-inverse navbar-fixed-top">
  <div class="container">
    <div class="navbar-header">

      <div class="row">
         <div class="col-sm-4">
      
            <a class="navbar-brand" href="index.php ">Target Aggregator</a>
          </div>
       
          <div class= "col-sm-8">
                
                      <form role="search" class="navbar-form " method="POST" action="results_display.php">
                          <div class="form-group" >
                              <input type="text" id="diff_address" name="location"  placeholder="change location.." class="form-control" style="width:100%;">
                          </div>

                          
                      </form>
            </div>
        </div>
    
    </div>
  </div>
</nav>





    <div class="container row" id="results" style="margin-top:120px;">

      <div class="col-sm-12 col-md-6 col-xs-12 col-lg-6 " >
      <br>
                     <div class='container-fluid' style='font-family:'Marcellus',serif;'>
                        <b><i>We are showing results for this location(local embassy)</b></i>
                     </div><br><br><b>We were able to show only these many results.</b><br><br><br><br>      
        
      </div>

      <div class="col-md-6  col-lg-6 hidden-xs hidden-sm "  id="map" style="position:relative">
                                        
                                                    
                                                      <div class="fixedContainer">
                                                      <iframe 
                                                        width="650"
                                                        height="460"                                                        
                                                        frameborder="0" style="border:0"
                                                        src="https://www.google.com/maps/embed/v1/place?key=AIzaSyAnPd6rDXQ8pUSBOkvy5TCI5PCDUFQXTdk
                                                          &q=local embassy" allowfullscreen>

                                                      </iframe></div>                                </div>      

  </div>
  <div class="col-xs-12 col-sm-12 hidden-md hidden-lg"  id="map" style="position:relative">

              
                                                    
                                                      <div class="container-fluid">
                                                      <iframe 
                                                        width="380"
                                                        height="300"                                                        
                                                        frameborder="0" style="border:0"
                                                        src="https://www.google.com/maps/embed/v1/place?key=AIzaSyAnPd6rDXQ8pUSBOkvy5TCI5PCDUFQXTdk
                                                          &q=local embassy" allowfullscreen>

                                                      </iframe></div>   </div>     
  


<footer class=" hidden-xs hidden-sm" id="lg_devices_foot" style="position:fixed;">
  
    <div class="col-sm-4 col-md-4 col-lg-4 col-xs-12 ">                  
    </div>
    <div class="col-sm-4 col-md-4 col-lg-4 ">              
    </div>
     <div class="col-sm-4 col-md-4 col-lg-4 col-xs-12"  > 
     </div> 
  
        
</footer>


<footer class="container-fluid hidden-md hidden-lg" id="sm_devices_foot">
  
    <div class="col-sm-4 col-md-4 col-lg-4 col-xs-12 ">                  
    </div>
    <div class="col-sm-4 col-md-4 col-lg-4 ">              
    </div>
     <div class="col-sm-4 col-md-4 col-lg-4 col-xs-12"  > 
     </div> 
  
        
</footer>




 


</body>
</html>
