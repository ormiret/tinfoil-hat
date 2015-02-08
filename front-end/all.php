<?php



require_once('common.php');



/*
http://tinfoil.bodaegl.com/api/all
*/

$data_array = get_all_json_as_array();

$title_count_array_trim = get_popular_words_as_array($data_array);

#$dump = print_r( $data_array, TRUE );


print_common_header($app_title);


?>
        <div class="col-sm-3 col-md-2 sidebar">
          <h3 class="sub-header">Most Popular Words</h3>
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Word</th>
                  <th>Count</th>
                </tr>
              </thead>
              <tbody>        
              <?php
              foreach ($title_count_array_trim as $title_text => $title_count) {
                ?>
                <tr>
                  <td><?php echo $title_text; ?></td>
                  <td><?php echo $title_count ?></td>  
                </tr>                         
                <?php
              }
              ?>
              </tbody>
            </table>
          </div>              
        </div>
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <h1 class="page-header">Dashboard</h1>
          
          <h2 class="sub-header">Section title</h2>
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>body</th>
                  <th>body_req_id</th>
                  <th>id</th>
                  <th>title</th>
                  <th>type</th>
                </tr>
              </thead>
              <tbody>
              <?php
              foreach ($data_array as $data_item) {
                ?>
                <tr>
                  <td><?php echo $data_item->body; ?></td>
                  <td><?php echo $data_item->body_req_id ?></td>
                  <td><?php echo $data_item->id ?></td>
                  <td><?php echo $data_item->title ?></td>
                  <td><?php echo $data_item->type ?></td>    
                </tr>                         
                <?php
              }
              ?>
              </tbody>
            </table>
          </div>
        </div>

<?php


print_common_footer();

?>

