<!doctype html>

<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="description" content="InTeXration">
	<meta name="author" content="InTeXration">

	<title>{{repo}} - {{name}}</title>

	<link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{base_url}}css/style.css">
</head>

<body>
    %include navigation base_url=base_url

    <div class="container">
        % if len(errors) > 0:
        <div class="callout callout-error">
            <h1>Errors</h1>
            <div class="log">
                % for line in errors:
                {{line}} <br/>
                % end
            </div>
        </div>
        % end
        % if len(warnings) > 0:
        <div class="callout callout-warning">
            <h1>Warnings</h1>
            <div class="log">
                % for line in warnings:
                {{line}} <br/>
                % end
            </div>
        </div>
        % end
        <div id="all" class="callout callout-info">
            <h1>Log</h1>
            <div class="log">
                % for line in all:
                {{line}} <br/>
                % end
            </div>
        </div>
    </div>

    %include footer
</body>
</html>