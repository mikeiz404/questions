<!doctype html>
<html class="no-js" lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Questions</title>
    <link rel="stylesheet" href="${request.static_url('project:static/css/foundation.css')}" />
    <script src="${request.static_url('project:static/js/vendor/modernizr.js')}"></script>
  </head>
  <body>

    <div class="row">
        <div class="large-12 columns">
            ${next.body()}
        </div>
    </div>

    <script src="${request.static_url('project:static/js/vendor/jquery.js')}"></script>
    <script src="${request.static_url('project:static/js/foundation.min.js')}"></script>
    <script>
      $(document).foundation();
    </script>
  </body>
</html>
