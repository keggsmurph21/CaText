<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Settlers of Catan</title>
    <meta charset="utf-8">
    <script src="core/includes/d3.v2.min.js"></script>
    <link href="style.css" rel="stylesheet" type="text/css" />
  </head>

  <body>

    <?php
    require_once('core/includes/funcs.php');
    init_settings('setup/standard/'); // should eventually be able to change which style gets loaded

    $start = start_timer();
    ?>

  	<div class="container">
      <svg id="boardContainer" width=<?= get_setting('board_container_width') ?> height=<?= get_setting('board_container_height') ?>>
        <?php if (get_setting('background_style') == 'texture') { ?>
          <defs>
            <pattern id="lumber" x="0" y="0" patternUnites="userSpaceOnUse" width="100" height="100">
              <image x="0" y="0" width="168" height="194" href="./resources/tile_bkg_lumber.png"> </image>
            </pattern>
            <pattern id="grain" x="0" y="0" patternUnites="userSpaceOnUse" width="200" height="200">
              <image x="0" y="0" width="168" height="194" href="./resources/tile_bkg_grain.png"> </image>
            </pattern>
            <pattern id="wool" x="0" y="0" patternUnites="userSpaceOnUse" width="200" height="200">
              <image x="0" y="0" width="168" height="194" href="./resources/tile_bkg_wool.png"> </image>
            </pattern>
            <pattern id="brick" x="0" y="0" patternUnites="userSpaceOnUse" width="200" height="200">
              <image x="0" y="0" width="168" height="194" href="./resources/tile_bkg_brick.png"> </image>
            </pattern>
            <pattern id="ore" x="0" y="0" patternUnites="userSpaceOnUse" width="200" height="200">
              <image x="0" y="0" width="168" height="194" href="./resources/tile_bkg_ore.png"> </image>
            </pattern>
            <pattern id="desert" x="0" y="0" patternUnites="userSpaceOnUse" width="200" height="200">
              <image x="0" y="0" width="168" height="194" href="./resources/tile_bkg_desert.png"> </image>
            </pattern>
            <pattern id="ocean" x="0" y="0" patternUnites="userSpaceOnUse" width="200" height="200">
              <image x="0" y="0" width="168" height="194" href="./resources/tile_bkg_ocean.png"> </image>
            </pattern>
          </defs>
        <?php } ?>

        <?php $attempts = setup_board(); ?>

      </svg>
  	</div>

    <?php
    $time = stop_timer($start);

    if (get_setting('debug')) {
      echo 'Page generated in ' . $time . ' seconds (' . $attempts . ').';
    }
    ?>

  </body>

  <script>

  function init_board() {

    var roll_chips = d3.selectAll('.roll', '.roll_chip').on( 'click', roll_chip_clicked ); // maybe add these methods in later
    var edges = d3.selectAll('.edge').on( 'click', edge_clicked );

    var hex_data = { 'resource' : null, 'center' : {'x':0, 'y':0},
      'neighbors' : { '60' : null, '120' : null, '180' : null, '240' : null, '300' : null, '360' : null }};

    var hexes = d3.select('#boardContainer').selectAll('.hex').datum(hex_data).on('click', hex_get_resource_type);
    hexes.each( function(d) {
      d.resource = hex_get_resource_type(this);
      d.center = hex_get_center(this);
      //console.log(d);
      //console.log(this);
    });
    hexes.each( function(d) {
      var a = this; var a_data = d;
      hexes.each( function(d) {
        var b = this; var b_data = d;
        console.log(distance(a_data.center, b_data.center));
      })
    })

    var nodes = d3.selectAll('.node').on( 'click', node_clicked );


    //nodes.style('display','none');
  }

  function roll_chip_clicked() {
    console.log(this);
    return this;
  }

  function edge_clicked() {
    console.log(this);
    return this;
  }

  function hex_clicked() {
    //var resource = this.attr('id');
    return this;
  }

  function hex_get_resource_type(hex) {
    var id = d3.select(hex).attr('id');
    return id.split('-')[0];
  }

  function hex_get_center(hex) {
    var list = d3.select(hex).attr('points').split(' ');
    var x_list = [];
    var y_list = [];

    for (var i=0; i<list.length; i++) {
      if (i%2) {
        y_list.push(list[i]);
      } else {
        x_list.push(list[i]);
      }
    }

    return {'x' : average(x_list), 'y' : average(y_list)};
  }

  function node_clicked() {
    console.log(this);
    return this;
  }

  function average(list) {
    var acc = 0; var num = 0;

    for (var i=0; i<list.length; i++) {
      if (list[i].length) { // avoid NaN issues with empty strings
        acc += parseFloat(list[i]);
        num ++;
      }
    }

    return acc/num;
  }

  function distance(a,b) {
    console.log(a,b);
    dx = b.x - a.x;
    dy = b.y - a.y;
    return (dx**2 + dy**2)**0.5;
  }

  function take_turn() {
    console.log('take turn');
    play_dev_card();
    roll_dice();
    play_dev_card();
    trade();
    play_dev_card();
    build();
    play_dev_card();

    check_victory_points();
  }

  function play_dev_card() {
    console.log('play dev card');
    var type = 'progress_card'; // tmp
    if (type === 'victory_point') {
      console.log('victory_point');
    } else if (type === 'progress_card') {
      console.log('progress_card');
    } else if (type === 'knight') {
      console.log('knight');
    } else {
      console.log('warning: invalid dev card');
    }

    check_victory_points();
  }

  function roll_dice() {
    console.log('roll dice');
    var roll = 3; // tmp
    if (roll === 7) {
      force_discard_half();
      hex = move_robber();
      while (!is_valid_move_robber(hex)) {
        hex = move_robber();
      }
      steal_card();
    } else {
      collect_resources();
    }
  }

  function trade() {
    console.log('trade');
    trade_with_players();
    trade_with_bank();
  }

  function build() {
    console.log('build');

    check_victory_points();
  }

  function force_discard_half() {
    console.log('force discard half');
  }

  function move_robber() {
    console.log('move robber');
  }

  function is_valid_move_robber() {
    console.log('is valid move robber');
    return true;
  }

  function steal_card() {
    console.log('steal card');
  }

  function collect_resources() {
    console.log('collect resources');
  }

  function trade_with_players() {
    console.log('trade with players');
  }

  function trade_with_bank() {
    console.log('trade with bank');
  }

  function check_victory_points() {
    console.log('check victory points');
  }

  init_board();

  </script>

</html>
