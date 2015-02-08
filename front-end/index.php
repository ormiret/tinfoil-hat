<?php


require_once('common.php');


print_common_header($long_app_title);


?>

        <div class="col-md-3"> </div>
        <div class="col-sm-6">
          <h1 class="page-header"><?php echo $app_title?></h1>
          <div class="tinfoilhat_search">
            <input id="term" type="text" placeholder="Add A Term"> <br/>
            <input id="location" type="text" class="typeahead" placeholder="Add A Location"/> <br/>
            <input id="from_day" class="date2" type="text" placeholder="DD"/> 
            <input id="from_month" class="date2" type="text" placeholder="MM"/> 
            <input id="from_year" class="date4" type="text" placeholder="YYYY"/> 
            -
            <input id="to_day" class="date2" type="text" placeholder="DD"/> 
            <input id="to_month" class="date2" type="text" placeholder="MM"/> 
            <input id="to_year" class="date4" type="text" placeholder="YYYY"/> 
               
            <button class="glyphicon glyphicon-search"></button>
          </div>
        </div>
        <div class="col-md-3"> </div>
        
        
        <script>
        var substringMatcher = function(strs) {
          return function findMatches(q, cb) {
            var matches, substrRegex;

            // an array that will be populated with substring matches
            matches = [];

            // regex used to determine if a string contains the substring `q`
            substrRegex = new RegExp(q, 'i');

            // iterate through the pool of strings and for any string that
            // contains the substring `q`, add it to the `matches` array
            $.each(strs, function(i, str) {
              if (substrRegex.test(str)) {
                // the typeahead jQuery plugin expects suggestions to a
                // JavaScript object, refer to typeahead docs for more info
                matches.push({ value: str });
              }
            });

            cb(matches);
          };
        };

        var states = ['Aberdeen City','Aberdeenshire','Angus','Argyll & Bute','Comhairle nan Eilean Siar','Clackmannanshire','Dumfries and Galloway','Dundee','East Ayrshire','East Dunbartonshire','Edinburgh','East Lothian','East Renfrewshire','Falkirk','Fife','Glasgow','Highland','Inverclyde','Midlothian','Moray','North Ayrshire','North Lanarkshire','Orkney','Perth & Kinross','Renfrewshire','Scottish Borders','Shetland Islands','South Ayrshire','South Lanarkshire','Stirling','West Dunbartonshire','West Lothian'];

        $('#location').typeahead({
          hint: true,
          highlight: true,
          minLength: 1
        },
        {
          name: 'states',
          displayKey: 'value',
          source: substringMatcher(states)
        });
        </script>
<?php


print_common_footer();

?>

