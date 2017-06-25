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

    <?php // timing stuff
    $start = start_timer();
    ?>

    <?php
    require_once('core/includes/funcs.php');
    init_settings('setup/standard/'); // should eventually be able to change which style gets loaded
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
      echo 'Page generated in ' . $total_time . ' seconds (' . $attempts . ').';
    }
    ?>

  </body>

  <script>

  function take_turn() {
    console.log('take turn');
    play_dev_card();
    roll_dice();
    play_dev_card();
    trade();
    play_dev_card();
    build();
    play_dev_card();
  }

  function play_dev_card() {
    console.log('play dev card');
  }

  function roll_dice() {
    console.log('roll dice');
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

  roll_chips = d3.selectAll('.roll', '.roll_chip');
  edges = d3.selectAll('.edge');
  hexes = d3.selectAll('.hex');
  nodes = d3.selectAll('.node');

  nodes.style('display','none');

  </script>

</html>
