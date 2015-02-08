<?php


require_once('common.php');


print_common_header($long_app_title);


?>
        <div class="col-md-2"> </div>
        <div class="col-sm-8">
          <h1 class="page-header"><?php echo $app_title?></h1>
          
          <input id="term" type="text" placeholder="Add A Term"> <br/>
          <input id="location" type="text" placeholder="Add A Location"/> <br/>
          <input id="from_day" type="text" placeholder="DD"/> 
          <input id="from_month" type="text" placeholder="MM"/> 
          <input id="from_year" type="text" placeholder="YYYY"/> 
          -
          <input id="to_day" type="text" placeholder="DD"/> 
          <input id="to_month" type="text" placeholder="MM"/> 
          <input id="to_year" type="text" placeholder="YYYY"/> 
           
          <button class="glyphicon glyphicon-search"></button>

        </div>
        <div class="col-md-2"> </div>
<?php


print_common_footer();

?>

