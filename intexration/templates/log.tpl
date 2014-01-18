<!doctype html>

<html lang="en">
<head>
	<meta charset="utf-8">

	<title>{{repo}} - {{name}}</title>
	<meta name="description" content="LaTeX Log">
	<meta name="author" content="InTeXration">
    <link rel="stylesheet" href="{{root}}style.css">
</head>

<body>
<div class="container">
	<div class="callout callout-error">
		<h1>Errors</h1>
		<div class="log">
			% for line in errors:
			{{line}} <br/>
			% end
		</div>
	</div>
	<div class="callout callout-warning">
		<h1>Warnings</h1>
		<div class="log">
			% for line in warnings:
			{{line}} <br/>
			% end
		</div>
	</div>

	<div id="all" class="callout callout-info">
		<h1>Log</h1>
		<div class="log">
			% for line in all:
			{{line}} <br/>
			% end
		</div>
	</div>
</div>

</body>
</html>