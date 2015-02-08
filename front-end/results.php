<?php



require_once('common.php');


$query = $_GET["term"];
$location = $_GET["location"];


$data_array = get_results_json_as_array($query, $location);

$title_count_array_trim = get_popular_words_as_array($data_array);

#$dump = print_r( $data_array, TRUE );


print_common_header($app_title);


?>
        <div class="col-sm-3 col-md-2 sidebar">
          <h3 class="sub-header">Most Popular Words in Results</h3>
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
              foreach ($title_count_array_trim as $word_text => $word_count) {
                ?>
                <tr>
                  <td><?php echo $word_text; ?></td>
                  <td><?php echo $word_count ?></td>  
                </tr>                         
                <?php
              }
              ?>
              </tbody>
            </table>
          </div>              
        </div>
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <h1 class="page-header">Results for "<?php echo $query; ?>"</h1>
          
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>title</th>
                  <th>body</th>
                  <th>body_name</th>                  
                  <th>body_req_id</th>
                  <th>intro</th>   
                  <th>doc id</th>                   
                  <th>link</th>                                        
                  <th>id</th>
                  <th>resp date</th>
                  <th>sub date</th>
                  <th>tags</th>                                                      
                  <th>type</th>
                </tr>
              </thead>
              <tbody>
              <?php
              foreach ($data_array as $data_item) {
                ?>
                <tr>            
                  <td><?php echo $data_item->title ?></td>
                  <td><?php echo $data_item->body; ?></td>
                  <td><?php echo $data_item->body_name ?></td>
                  <td><?php echo $data_item->body_req_id ?></td>
                  <td><?php echo $data_item->docs[0]->text_start ?></td>
                  <td><img src="css/DOC_Icon.svg"<?php echo $data_item->docs[0]->url ?></td>                  
                  <td><?php echo $data_item->docs[0]->id ?></td>
                  </td>
                  <td><?php echo $data_item->id ?></td>
                  <td><?php echo $data_item->response_date ?></td>
                  <td><?php echo $data_item->submission_date ?></td>
                  <td><span class="tag"><?php echo implode("</span>, <span class=\"tag\">", $data_item->tags) ?></span></td>

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

