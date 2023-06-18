<!DOCTYPE html>
<html lang="en">
<head>
  <title>Target Aggregator</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="css/bootstrap.min.css">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <link href="https://fonts.googleapis.com/css?family=Bungee+Inline" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css?family=Architects+Daughter" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css?family=Luckiest+Guy" rel="stylesheet"> 
  <link href="https://fonts.googleapis.com/css?family=Quantico" rel="stylesheet"> 
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.2/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
  <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCDmFqQa3GmRdYRtITKJnv3qF3-tsL5H2A&v=3.exp&sensor=false&libraries=places"></script>
  <script type="text/javascript">
               function initialize() {
                       var input = document.getElementById('place_location');
                       var autocomplete = new google.maps.places.Autocomplete(input);
               }
               google.maps.event.addDomListener(window, 'load', initialize);
       </script>
  
  <script src="https://use.fontawesome.com/4ade0e5ef1.js"></script>
  <style type="text/css">

    .jumbotron 
    {
             
      /*margin-top: 50px;*/
      color: black;
      background: url("jumbotron_img/map2.jpg") no-repeat center center;       
     -webkit-background-size: 100% 100%;
     -moz-background-size: 100% 100%;
     -o-background-size: 100% 100%;
      background-size: 100% 100%;

     }

     .navbar{
    background-color: transparent;
    border-style: none;    
    color:green;
    height: 50px;
    text-align: center;
    font-family: 'Luckiest Guy', cursive;
    font-size: 20px;
      


     }

     .active{
      background-color: green;
     } 
    footer
    {
      background-color: #121212;
      margin-top:30px;
      position:relative;
      padding: 10px;           
      height:60px;
      color: white;
      position: relative;
      right: 0;
      bottom: 0;
      left: 0;
    }


     


  </style>
 </head>

 <body>
  
  <nav class="navbar navbar-inverse navbar-fixed-top">
  
      <a class="navbar-brand" href="#" >Home</a>
      <a class="navbar-brand navbar-right" href="about.php"  >About</a>
      <a class="navbar-brand navbar-right" href="map-update.php"  >Map Update</a>
    
  </nav>


<div class="jumbotron">
  <div class="container-fluid text-center" style="height: 470px; ">
    <h1 style="color:white; font-family:'Bungee Inline', cursive; margin-top:100px;">Target Aggregator</h1> <hr>     
    <p style="color:white; font-family:'Architects Daughter', cursive;">The intergalactic ministry of spies invites you to enter and search for targeting details here.</p>
  </div>
</div>


<div class="container-fluid text-center" style="background-color:#A7C2E2; ">
  <div id="brief">
  <h2 style="text-align: center; color:#080C17;font-family: 'Quantico', sans-serif;  ";>Choose the target you want to find..</h2>
  <p style="font-size: 18px; ">
    
  </p>  
  </div>
</div>


 <div class="container" style="margin-top:50px;">
        <!-- form begins-->
        <form role="form"  method="POST" action="results_display.php">
          
          <div class="form-group" >
            <input type="text" class="form-control" name="location" id="place_location" placeholder="Enter the address of the target.."  style="align:center"/>                               
          </div>
          
          <div class="form-group">
            <select class="form-control" name="keyword">            

              <option value="Barracks" >Barracks</a></option><!--2-->
	      <option value="Space Station" >Space Station</a></option><!--2-->
	      <option value="Enemy HQ" >Enemy HQ</a></option><!--2-->
	      <option value="Weapons Store" >Weapons Store</a></option><!--2-->
	      <option value="Barracks" >Inter Galactic Embassy</a></option><!--2-->

              
            </select> 
 
          </div>

          <div class="col-xs-6 col-sm-6 col-md-6">
              <input type="submit" name="submit_mes" value="SEARCH" class="btn btn-lg btn-success btn-block"><hr>
          </div>

        </form>
        <!-- end form-->

 </div>      

       

<footer class="container-fluid" >
  <div class="row">
    
     <div class="col-sm-4">                  
    </div>
    <div class="col-sm-4">              
    </div>
     <div class="col-sm-4"  > 
     </div> 
        
</footer>





</body>
</html>
