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
    ?>

  	<div class="container">
      <svg id="boardContainer" width=<?= get_setting('board_container_width') ?> height=<?= get_setting('board_container_height') ?>>
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

        <?php setup_board(); ?>

      </svg>
  	</div>

  </body>

  <script>

  </script>

</html>
