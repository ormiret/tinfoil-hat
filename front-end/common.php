<?php

# generic common vars
$app_title = "TinFOIlhat";
$long_app_title = "TinFOIlhat - Freedom of Information Search Engine";


# 
function get_all_json_as_array() {

    # get the json
    $json_data = file_get_contents ( "http://tinfoil.bodaegl.com/api/all" );

    # decode it
    $data_array = json_decode( $json_data );

    # pull out the child that has the data in it    
    $data_array = $data_array->requests;

    return $data_array;
}



#
function get_popular_words_as_array($data_array) {

    $title_all_string = "";

    foreach ($data_array as $data_item) {
        $title_all_string .= $data_item->title . " ";
    }

    $title_all_array = explode(" ", $title_all_string);

    $common_words = array('and', 'if', 'in', 'of', 'an', 'my', 'to', 'for', '0');

    $title_count_array = array();
    foreach ($title_all_array as $title_all_item) {
        if ( in_array( $title_all_item, $common_words) ) {
            # ignore this one, it's common
        
        } else {
            if ( array_key_exists( $title_all_item, $title_count_array )  ) {
                # counted this before, increment it
                $title_count_array[$title_all_item]++;
                
            } else {
                # not counted this before
                $title_count_array[$title_all_item] = 1;
            
            }
        }
    }

    arsort($title_count_array);

    #echo "<pre>" . print_r( $title_count_array, TRUE ) . "</pre>";

    # trim it down
    $title_count_array_trim = array_slice($title_count_array, 0, 20);
    
    return $title_count_array_trim;


}





#
function print_common_header($app_title) {
?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="favicon.ico">

    <title><?php echo $app_title?></title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/tinfoil.css" rel="stylesheet">
    <link href='http://fonts.googleapis.com/css?family=Roboto+Condensed:400,400italic' rel='stylesheet' type='text/css'>
    
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/typeahead.jquery.js"></script>    
        
  </head>

  <body>

    <nav class="navbar navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#"><?php echo $app_title?></a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav navbar-right">
            <li><a href="https://ico.org.uk/for-organisations/guide-to-freedom-of-information/what-is-the-foi-act/" target="_blank">FOI?</a></li>
            <li><a href="http://codethecity.org/" target="_blank">codethecity.org</a></li>
            <li><a href="https://github.com/ormiret/tinfoil-hat" target="_blank">On GitHub</a></li>
          </ul>
          <form class="navbar-form navbar-right">
            <input type="text" class="form-control" placeholder="Search...">
          </form>
        </div>
      </div>
    </nav>

    <div class="container-fluid">
      <div class="row">

<?php
}



#
function print_common_footer() {
?>
      </div>
    </div>



    
    
    

  </body>
</html>
<?php
}



?>
